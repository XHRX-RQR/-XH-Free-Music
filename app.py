import asyncio
import logging
import os
import re
import requests
from urllib.parse import quote
import pygame
import subprocess
import wave
import struct

# 尝试导入音频处理库（按优先级尝试）
AUDIO_CONVERTER = None

# 方案1: 尝试使用 moviepy（推荐，无需ffmpeg）
try:
    from moviepy import AudioFileClip
    AUDIO_CONVERTER = 'moviepy'
except ImportError:
    pass

# 方案2: 尝试使用 pydub（需要ffmpeg）
if not AUDIO_CONVERTER:
    try:
        from pydub import AudioSegment
        import shutil
        if shutil.which('ffmpeg'):
            AUDIO_CONVERTER = 'pydub'
    except ImportError:
        pass

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

# 下载路径
DOWNLOAD_PATH = "./bilibili_music"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def clean_text(text):
    """清理文本中的HTML标签和特殊字符"""
    text = text.replace("<em class=\"keyword\">", "").replace("</em>", "")
    text = re.sub(r'&[a-z]+;', '', text)  # 移除 HTML 实体如 &amp;
    return text.strip()

def is_live_or_concert(title):
    """判断是否为演唱会、直播等非官方版本"""
    keywords = ['演唱会', '现场', '直播', 'live', 'concert', '跨年', '晚会', '舞台', '音乐节']
    title_lower = title.lower()
    return any(kw in title_lower for kw in keywords)

def is_cover_or_remix(title):
    """判断是否为翻唱、remix等改编版本"""
    keywords = ['翻唱', '翻唱版', 'cover', 'remix', '改编', '伴奏', '卡拉ok', '纯音乐']
    title_lower = title.lower()
    return any(kw in title_lower for kw in keywords)

def calculate_match_score(title, keyword):
    """计算标题与关键词的匹配分数（0-100）"""
    clean_title = clean_text(title).lower()
    keyword = keyword.lower().strip()
    score = 0
    
    # 1. 完整匹配（50分）
    if keyword in clean_title:
        score += 50
    
    # 2. 分词匹配（每个词10分，最多30分）
    keywords = keyword.split()
    matched_words = sum(1 for kw in keywords if kw in clean_title)
    score += min(matched_words * 10, 30)
    
    # 3. 包含"官方"、"MV"、"正式版"等关键词（10分）
    if any(kw in clean_title for kw in ['官方', 'official', 'mv', '正式版', '完整版']):
        score += 10
    
    # 4. 包含歌手名或歌曲名在开头（10分）
    if keywords and clean_title.startswith(keywords[0]):
        score += 10
    
    # 惩罚项：
    # - 演唱会/直播版本（-30分）
    if is_live_or_concert(clean_title):
        score -= 30
    
    # - 翻唱/改编版本（-20分）
    if is_cover_or_remix(clean_title):
        score -= 20
    
    # - 标题过长（超过50个字符 -10分）
    if len(clean_title) > 50:
        score -= 10
    
    return max(0, min(100, score))  # 限制在0-100之间

def title_contains_keyword(title, keyword):
    """检查标题是否包含搜索关键词（基于匹配分数）"""
    score = calculate_match_score(title, keyword)
    return score >= 30  # 分数大于等于30认为匹配

def search_bilibili(song_name, max_results=20):
    """使用B站搜索API获取歌曲视频链接"""
    search_keyword = quote(song_name)
    api_url = f"https://api.bilibili.com/x/web-interface/search/type?keyword={search_keyword}&search_type=video&order=click&page=1&pagesize={max_results}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com",
        "Accept": "application/json, text/plain, */*",
    }
    
    session = requests.Session()
    try:
        # 先访问B站首页，获取cookie
        session.get("https://www.bilibili.com", headers=headers, timeout=10)
        
        # 发送搜索API请求
        response = session.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
    except requests.exceptions.RequestException as e:
        log.error(f"搜索请求失败：{str(e)}")
        return None, None
    except ValueError as e:
        log.error(f"JSON解析失败：{str(e)}")
        return None, None

    # 解析API响应
    if data.get("code") != 0:
        log.error(f"API返回错误：{data.get('message', '未知错误')}")
        return None, None
    
    results = data.get("data", {}).get("result", [])
    if not results:
        log.error(f"未找到与'{song_name}'相关的视频")
        return None, None
    
    # 计算每个视频的匹配分数并排序
    scored_videos = []
    for idx, video in enumerate(results):
        title = video.get("title", "")
        clean_title = clean_text(title)
        bvid = video.get("bvid")
        
        if not bvid:
            continue
        
        score = calculate_match_score(title, song_name)
        scored_videos.append({
            'index': idx + 1,
            'bvid': bvid,
            'title': clean_title,
            'score': score,
            'play': video.get('play', 0),  # 播放量
        })
        
        log.debug(f"[{idx + 1}] 分数:{score} - {clean_title}")
    
    # 按分数降序排序，分数相同则按播放量排序
    scored_videos.sort(key=lambda x: (x['score'], x['play']), reverse=True)
    
    # 选择分数最高的视频
    if scored_videos and scored_videos[0]['score'] >= 30:
        best_match = scored_videos[0]
        video_url = f"https://www.bilibili.com/video/{best_match['bvid']}"
        log.info(f"找到最佳匹配视频 [评分:{best_match['score']}]：{best_match['title']}")
        log.info(f"视频链接：{video_url}")
        return video_url, best_match['title']
    
    # 如果没有高分匹配的，使用第一个结果并警告
    if scored_videos:
        fallback = scored_videos[0]
        video_url = f"https://www.bilibili.com/video/{fallback['bvid']}"
        log.warning(f"未找到高质量匹配（最高分:{fallback['score']}），使用：{fallback['title']}")
        log.info(f"视频链接：{video_url}")
        return video_url, fallback['title']
    
    log.error("未能获取有效视频")
    return None, None

def get_video_audio_url(bvid):
    """获取B站视频的音频流URL"""
    video_url = f"https://www.bilibili.com/video/{bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": video_url,
    }
    
    # 获取视频播放信息API
    play_info_url = f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid=0&qn=64&fnval=16"
    
    try:
        response = requests.get(play_info_url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") != 0:
            log.error(f"获取播放信息失败：{data.get('message', '未知错误')}")
            return None
        
        # 提取音频URL
        audio_list = data.get("data", {}).get("dash", {}).get("audio", [])
        if not audio_list:
            log.error("未找到音频流")
            return None
        
        # 选择第一个音频流（通常是最高质量）
        audio_url = audio_list[0].get("baseUrl") or audio_list[0].get("base_url")
        return audio_url
        
    except Exception as e:
        log.error(f"获取音频URL失败：{str(e)}")
        return None

def convert_to_mp3(input_path, output_path):
    """使用可用的方法将音频转换为MP3格式"""
    if not AUDIO_CONVERTER:
        log.warning("未找到可用的音频转换工具")
        log.info("建议安装: pip install moviepy")
        return input_path
    
    try:
        log.info(f"正在转换为 MP3 格式（使用 {AUDIO_CONVERTER}）...")
        
        if AUDIO_CONVERTER == 'moviepy':
            # 使用 moviepy 转换（推荐方案）
            from moviepy import AudioFileClip
            audio_clip = AudioFileClip(input_path)
            audio_clip.write_audiofile(output_path, codec='libmp3lame', bitrate='192k', logger=None)
            audio_clip.close()
            
        elif AUDIO_CONVERTER == 'pydub':
            # 使用 pydub 转换（需要ffmpeg）
            from pydub import AudioSegment
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format="mp3", bitrate="192k")
        
        # 删除原文件
        if os.path.exists(input_path) and input_path != output_path:
            os.remove(input_path)
            log.info(f"已删除临时文件：{os.path.basename(input_path)}")
        
        log.info(f"转换成功：{os.path.basename(output_path)}")
        return output_path
        
    except Exception as e:
        log.error(f"转换失败：{str(e)}")
        log.info("将使用原始格式")
        return input_path

async def download_audio_simple(video_url, song_name, video_title):
    """下载音频并转换为MP3格式"""
    # 从视频URL提取BV号
    bvid = video_url.split("/")[-1].split("?")[0]
    
    log.info(f"正在下载音频...")
    
    # 使用yt-dlp下载音频
    safe_filename = "".join(c for c in song_name if c.isalnum() or c in (' ', '-', '_')).strip()
    
    args = [
        "yt-dlp",
        "--no-playlist",
        "-f", "bestaudio",  # 下载最佳音频
        "--paths", DOWNLOAD_PATH,
        "-o", f"{safe_filename}.%(ext)s",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "--referer", "https://www.bilibili.com/",
        video_url
    ]
    
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    if process.returncode != 0:
        error_msg = stderr.decode('utf-8', errors='ignore')
        log.error(f"下载失败：{error_msg}")
        return None
    
    # 查找下载后的文件
    audio_path = None
    for file in os.listdir(DOWNLOAD_PATH):
        if safe_filename in file and file.endswith(('.m4a', '.webm', '.opus', '.mp3')):
            audio_path = os.path.join(DOWNLOAD_PATH, file)
            break
    
    if not audio_path:
        # 兜底：取最新的音频文件
        audio_files = [f for f in os.listdir(DOWNLOAD_PATH) 
                      if f.endswith(('.m4a', '.webm', '.opus', '.mp3'))]
        if audio_files:
            audio_path = os.path.join(DOWNLOAD_PATH, 
                                     sorted(audio_files, 
                                           key=lambda x: os.path.getctime(os.path.join(DOWNLOAD_PATH, x)))[-1])
            log.warning(f"使用最新下载的音频文件：{audio_path}")
    
    if not audio_path or not os.path.exists(audio_path):
        log.error("未找到下载的音频文件")
        return None
    
    log.info(f"下载成功：{os.path.basename(audio_path)}")
    
    # 转换为MP3格式
    if not audio_path.endswith('.mp3'):
        mp3_path = os.path.join(DOWNLOAD_PATH, f"{safe_filename}.mp3")
        audio_path = convert_to_mp3(audio_path, mp3_path)
    
    return audio_path

def play_audio(audio_path):
    """使用pygame播放音频文件"""
    if not os.path.exists(audio_path):
        log.error(f"音频文件不存在：{audio_path}")
        return
    
    try:
        # 初始化pygame
        pygame.mixer.quit()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        
        # 加载并播放
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        log.info(f"正在播放：{os.path.basename(audio_path)}")
        log.info("按 Ctrl+C 停止播放")
        
        # 等待播放完成
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        log.info("播放完成")
        
    except Exception as e:
        log.error(f"播放失败：{str(e)}")
        log.info(f"你可以手动播放文件：{audio_path}")
    finally:
        pygame.mixer.quit()

async def main():
    """主函数"""
    print("=" * 60)
    print("B站音乐下载播放器（无需ffmpeg版本）")
    print("=" * 60)
    
    # 检查依赖
    import shutil
    if not shutil.which("yt-dlp"):
        log.error("缺少依赖：yt-dlp")
        log.error("请安装：pip install yt-dlp")
        return
    
    if not AUDIO_CONVERTER:
        log.warning("="*60)
        log.warning("未安装音频转换工具，将无法转换为 MP3 格式")
        log.warning("推荐安装：pip install moviepy")
        log.warning("或安装：pip install pydub（需要 ffmpeg）")
        log.warning("="*60)
    
    song_name = input("\n请输入歌曲名：").strip()
    if not song_name:
        log.error("歌曲名不能为空")
        return
    
    # 1. 搜索B站视频
    log.info(f"正在搜索：{song_name}")
    video_url, video_title = search_bilibili(song_name)
    if not video_url:
        return
    
    # 2. 下载音频
    audio_path = await download_audio_simple(video_url, song_name, video_title)
    if not audio_path:
        return
    
    # 3. 播放音频
    play_audio(audio_path)

if __name__ == "__main__":
    """
    安装依赖：
    pip install yt-dlp requests pygame moviepy
    
    说明：
    - 智能搜索：优先匹配官方MV，过滤演唱会、翻唱等版本
    - 音频转换：自动转换为 MP3 格式
      * 推荐方案：moviepy（无需 ffmpeg）
      * 备用方案：pydub + ffmpeg
    - 如果未安装转换工具，将保留原始格式（m4a/webm/opus）
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n已停止")




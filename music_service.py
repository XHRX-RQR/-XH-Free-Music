"""
音乐服务模块 - 核心业务逻辑
提供搜索、下载、音频处理功能
"""
import asyncio
import logging
import os
import re
import requests
from urllib.parse import quote
import shutil

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

# 音频转换器配置
AUDIO_CONVERTER = None

# 尝试导入音频处理库
try:
    from moviepy import AudioFileClip
    AUDIO_CONVERTER = 'moviepy'
except ImportError:
    try:
        from pydub import AudioSegment
        if shutil.which('ffmpeg'):
            AUDIO_CONVERTER = 'pydub'
    except ImportError:
        pass


class MusicService:
    """音乐服务类"""
    
    def __init__(self, download_path="./bilibili_music"):
        self.download_path = download_path
        os.makedirs(self.download_path, exist_ok=True)
    
    @staticmethod
    def clean_text(text):
        """清理文本中的HTML标签和特殊字符"""
        text = text.replace("<em class=\"keyword\">", "").replace("</em>", "")
        text = re.sub(r'&[a-z]+;', '', text)
        return text.strip()
    
    @staticmethod
    def is_live_or_concert(title):
        """判断是否为演唱会、直播等非官方版本"""
        keywords = ['演唱会', '现场', '直播', 'live', 'concert', '跨年', '晚会', '舞台', '音乐节']
        title_lower = title.lower()
        return any(kw in title_lower for kw in keywords)
    
    @staticmethod
    def is_cover_or_remix(title):
        """判断是否为翻唱、remix等改编版本"""
        keywords = ['翻唱', '翻唱版', 'cover', 'remix', '改编', '伴奏', '卡拉ok', '纯音乐']
        title_lower = title.lower()
        return any(kw in title_lower for kw in keywords)
    
    @staticmethod
    def calculate_match_score(title, keyword):
        """计算标题与关键词的匹配分数（0-100）"""
        clean_title = MusicService.clean_text(title).lower()
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
        
        # 惩罚项
        if MusicService.is_live_or_concert(clean_title):
            score -= 30
        
        if MusicService.is_cover_or_remix(clean_title):
            score -= 20
        
        if len(clean_title) > 50:
            score -= 10
        
        return max(0, min(100, score))
    
    def search_bilibili(self, song_name, max_results=20):
        """搜索B站音乐视频"""
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
            session.get("https://www.bilibili.com", headers=headers, timeout=10)
            response = session.get(api_url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
        except requests.exceptions.RequestException as e:
            log.error(f"搜索请求失败：{str(e)}")
            return []
        except ValueError as e:
            log.error(f"JSON解析失败：{str(e)}")
            return []
        
        if data.get("code") != 0:
            log.error(f"API返回错误：{data.get('message', '未知错误')}")
            return []
        
        results = data.get("data", {}).get("result", [])
        if not results:
            log.error(f"未找到与'{song_name}'相关的视频")
            return []
        
        # 计算每个视频的匹配分数并排序
        scored_videos = []
        for idx, video in enumerate(results):
            title = video.get("title", "")
            clean_title = self.clean_text(title)
            bvid = video.get("bvid")
            
            if not bvid:
                continue
            
            score = self.calculate_match_score(title, song_name)
            scored_videos.append({
                'index': idx + 1,
                'bvid': bvid,
                'title': clean_title,
                'score': score,
                'play': video.get('play', 0),
                'author': video.get('author', '未知'),
                'duration': self._format_duration(video.get('duration', '')),
                'pic': video.get('pic', ''),
                'video_url': f"https://www.bilibili.com/video/{bvid}"
            })
        
        # 按分数降序排序
        scored_videos.sort(key=lambda x: (x['score'], x['play']), reverse=True)
        
        return scored_videos
    
    @staticmethod
    def _format_duration(duration_str):
        """格式化时长"""
        if isinstance(duration_str, str) and ':' in duration_str:
            return duration_str
        elif isinstance(duration_str, int):
            minutes = duration_str // 60
            seconds = duration_str % 60
            return f"{minutes:02d}:{seconds:02d}"
        return "00:00"
    
    async def download_audio(self, video_url, song_name):
        """下载音频并转换为MP3格式"""
        try:
            bvid = video_url.split("/")[-1].split("?")[0]
            
            log.info("="*60)
            log.info(f"开始下载任务")
            log.info(f"歌曲名称: {song_name}")
            log.info(f"视频链接: {video_url}")
            log.info(f"BV号: {bvid}")
            log.info("="*60)
            
            # 安全文件名
            safe_filename = "".join(c for c in song_name if c.isalnum() or c in (' ', '-', '_')).strip()
            if not safe_filename:
                safe_filename = f"music_{bvid}"
            
            log.info(f"安全文件名: {safe_filename}")
            
            # 构建yt-dlp命令
            args = [
                "yt-dlp",
                "--no-playlist",
                "-f", "bestaudio",
                "--paths", self.download_path,
                "-o", f"{safe_filename}.%(ext)s",
                "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "--referer", "https://www.bilibili.com/",
                "--no-warnings",
                video_url
            ]
            
            log.info(f"执行命令: {' '.join(args)}")
            
            process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            log.info("等待下载完成...")
            stdout, stderr = await process.communicate()
            
            stdout_text = stdout.decode('utf-8', errors='ignore') if stdout else ''
            stderr_text = stderr.decode('utf-8', errors='ignore') if stderr else ''
            
            if stdout_text:
                log.info(f"标准输出: {stdout_text[:500]}")
            if stderr_text:
                log.warning(f"标准错误: {stderr_text[:500]}")
            
            if process.returncode != 0:
                log.error(f"yt-dlp 返回错误代码: {process.returncode}")
                log.error(f"错误信息: {stderr_text}")
                return None
            
            # 查找下载后的文件
            log.info(f"搜索下载文件，目录: {self.download_path}")
            audio_path = None
            
            for file in os.listdir(self.download_path):
                log.info(f"检查文件: {file}")
                if safe_filename in file and file.endswith(('.m4a', '.webm', '.opus', '.mp3')):
                    audio_path = os.path.join(self.download_path, file)
                    log.info(f"找到匹配文件: {file}")
                    break
            
            if not audio_path or not os.path.exists(audio_path):
                log.error("未找到下载的音频文件")
                log.error(f"目录内容: {os.listdir(self.download_path)}")
                return None
            
            log.info(f"✅ 下载成功：{os.path.basename(audio_path)}")
            log.info(f"文件大小: {os.path.getsize(audio_path) / 1024 / 1024:.2f} MB")
            
            # 如果已经是MP3，直接返回
            if audio_path.endswith('.mp3'):
                log.info("文件已经是MP3格式，无需转换")
                return audio_path
            
            # 转换为MP3格式
            log.info("开始转换为MP3格式...")
            mp3_path = os.path.join(self.download_path, f"{safe_filename}.mp3")
            audio_path = self.convert_to_mp3(audio_path, mp3_path)
            
            log.info("="*60)
            log.info(f"✅ 任务完成: {os.path.basename(audio_path)}")
            log.info("="*60)
            
            return audio_path
            
        except Exception as e:
            log.error(f"下载过程发生异常: {str(e)}")
            import traceback
            log.error(traceback.format_exc())
            return None
    
    def convert_to_mp3(self, input_path, output_path):
        """将音频转换为MP3格式"""
        if not AUDIO_CONVERTER:
            log.warning("未找到可用的音频转换工具")
            return input_path
        
        try:
            log.info(f"正在转换为 MP3 格式（使用 {AUDIO_CONVERTER}）...")
            
            if AUDIO_CONVERTER == 'moviepy':
                from moviepy import AudioFileClip
                audio_clip = AudioFileClip(input_path)
                audio_clip.write_audiofile(output_path, codec='libmp3lame', bitrate='192k', logger=None)
                audio_clip.close()
                
            elif AUDIO_CONVERTER == 'pydub':
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
            return input_path
    
    def get_downloaded_files(self):
        """获取已下载的音乐文件列表"""
        if not os.path.exists(self.download_path):
            return []
        
        files = []
        for filename in os.listdir(self.download_path):
            # 支持多种音频格式
            if filename.endswith(('.mp3', '.m4a', '.webm', '.opus')):
                filepath = os.path.join(self.download_path, filename)
                files.append({
                    'name': filename,
                    'path': filepath,
                    'size': os.path.getsize(filepath),
                    'modified': os.path.getmtime(filepath)
                })
        
        # 按修改时间倒序排序
        files.sort(key=lambda x: x['modified'], reverse=True)
        return files

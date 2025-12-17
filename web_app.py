# 免费音乐网站 - Flask Web应用
# 基于B站音频提取功能的在线音乐平台
# 支持多用户注册登录

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, redirect, url_for, session
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import asyncio
import os
import logging
from functools import wraps
from datetime import datetime
from music_service import MusicService
from models import db, User, Music

# 配置日志
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'  # 生产环境请修改！
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///freemusic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 最大500MB
app.config['DOWNLOAD_FOLDER'] = './bilibili_music'

# 初始化数据库
db.init_app(app)

# 初始化登录管理器
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录'

# 初始化音乐服务
music_service = MusicService(download_path="./bilibili_music")


@login_manager.user_loader
def load_user(user_id):
    """加载用户"""
    return User.query.get(int(user_id))


def login_required_api(f):
    """API接口登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                'success': False,
                'message': '请先登录',
                'need_login': True
            }), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    # 主页（需要登录）
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/test')
def test():
    """测试页面"""
    return render_template('test.html')


@app.route('/api/search', methods=['POST'])
def search_music():
    """搜索音乐API"""
    try:
        data = request.get_json()
        keyword = data.get('keyword', '').strip()
        
        if not keyword:
            return jsonify({
                'success': False,
                'message': '请输入搜索关键词'
            }), 400
        
        log.info(f"搜索关键词: {keyword}")
        
        # 搜索音乐
        results = music_service.search_bilibili(keyword, max_results=20)
        
        if not results:
            return jsonify({
                'success': False,
                'message': '未找到相关音乐'
            })
        
        return jsonify({
            'success': True,
            'data': results,
            'total': len(results)
        })
        
    except Exception as e:
        log.error(f"搜索失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'搜索失败: {str(e)}'
        }), 500


@app.route('/api/cache', methods=['POST'])
@login_required_api
def cache_music():
    """播放音乐API（下载、播放后删除文件，只保存元数据）"""
    try:
        data = request.get_json()
        video_url = data.get('video_url', '')
        title = data.get('title', '未知歌曲')
        artist = data.get('artist', '')
        bvid = data.get('bvid', '')
        
        log.info("="*70)
        log.info("🎵 播放音乐请求")
        log.info(f"  - 用户: {current_user.username}")
        log.info(f"  - 视频URL: {video_url}")
        log.info(f"  - 标题: {title}")
        log.info(f"  - 歌手: {artist}")
        log.info("="*70)
        
        if not video_url:
            log.error("❌ 视频链接为空")
            return jsonify({
                'success': False,
                'message': '视频链接不能为空'
            }), 400
        
        # 检查数据库中是否已有此音乐记录（当前用户）
        existing_music = Music.query.filter_by(
            user_id=current_user.id,
            video_url=video_url
        ).first()
        
        # 构建临时文件名
        if artist:
            filename_base = f"{current_user.username}_{artist} - {title}"
        else:
            filename_base = f"{current_user.username}_{title}"
        
        # 安全文件名（移除非法字符，保留中文）
        safe_filename = "".join(
            c for c in filename_base 
            if c.isalnum() or c in (' ', '-', '_') or '\u4e00' <= c <= '\u9fff'
        ).strip()
        if not safe_filename:
            safe_filename = f"{current_user.username}_music_{video_url.split('/')[-1]}"
        
        log.info(f"📁 临时文件名: {safe_filename}")
        
        # 下载音频
        log.info("📥 开始下载音频...")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            audio_path = loop.run_until_complete(
                music_service.download_audio(video_url, safe_filename)
            )
        finally:
            loop.close()
        
        if not audio_path:
            log.error("❌ 下载音频失败，返回 None")
            return jsonify({
                'success': False,
                'message': '音频下载失败，请检查视频链接是否有效或稍后重试'
            }), 500
        
        # 获取文件名
        filename = os.path.basename(audio_path)
        
        # 更新或创建数据库记录
        if existing_music:
            log.info(f"✅ 更新数据库记录: {existing_music.title}")
            existing_music.play_count += 1
            existing_music.played_at = datetime.utcnow()
            db.session.commit()
            music_record = existing_music
        else:
            log.info("🎵 创建新的数据库记录")
            new_music = Music(
                user_id=current_user.id,
                title=title,
                artist=artist,
                video_url=video_url,
                bvid=bvid,
                play_count=1,
                played_at=datetime.utcnow()
            )
            db.session.add(new_music)
            db.session.commit()
            music_record = new_music
        
        log.info("="*70)
        log.info(f"✅ 下载成功: {filename}")
        log.info(f"  - 数据库ID: {music_record.id}")
        log.info(f"  - 播放次数: {music_record.play_count}")
        log.info("⚠️  注意：音频播放结束后将自动删除，节省空间")
        log.info("="*70)
        
        # 返回临时文件路径
        response_data = music_record.to_dict()
        response_data['filename'] = filename
        response_data['play_url'] = f'/api/stream/{filename}'
        response_data['temp_file'] = True  # 标记为临时文件
        
        return jsonify({
            'success': True,
            'message': '下载成功，开始播放',
            'data': response_data
        })
        
    except Exception as e:
        db.session.rollback()
        import traceback
        log.error("="*70)
        log.error("❌ 播放失败")
        log.error(f"  - 错误: {str(e)}")
        log.error(f"  - 堆栈:\n{traceback.format_exc()}")
        log.error("="*70)
        return jsonify({
            'success': False,
            'message': f'播放失败: {str(e)}'
        }), 500


@app.route('/api/download', methods=['POST'])
def download_music():
    """下载音乐API"""
    try:
        data = request.get_json()
        video_url = data.get('video_url', '')
        title = data.get('title', '未知歌曲')
        
        if not video_url:
            return jsonify({
                'success': False,
                'message': '视频链接不能为空'
            }), 400
        
        log.info(f"开始下载: {title}")
        
        # 异步下载音频
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_path = loop.run_until_complete(
            music_service.download_audio(video_url, title)
        )
        loop.close()
        
        if not audio_path:
            return jsonify({
                'success': False,
                'message': '下载失败'
            }), 500
        
        # 返回下载结果
        filename = os.path.basename(audio_path)
        return jsonify({
            'success': True,
            'message': '下载成功',
            'data': {
                'filename': filename,
                'path': f'/api/stream/{filename}',
                'download_url': f'/api/file/{filename}'
            }
        })
        
    except Exception as e:
        log.error(f"下载失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'下载失败: {str(e)}'
        }), 500


@app.route('/api/stream/<filename>')
def stream_music(filename):
    """音频流播放API"""
    try:
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        log.info(f"请求播放文件: {filename}")
        log.info(f"文件路径: {file_path}")
        
        if not os.path.exists(file_path):
            log.error(f"文件不存在: {file_path}")
            return jsonify({
                'success': False,
                'message': '文件不存在'
            }), 404
        
        # 检查文件大小
        file_size = os.path.getsize(file_path)
        log.info(f"文件大小: {file_size / 1024 / 1024:.2f} MB")
        
        # 设置正确的MIME类型
        mimetype = 'audio/mpeg'
        if filename.endswith('.m4a'):
            mimetype = 'audio/mp4'
        elif filename.endswith('.webm'):
            mimetype = 'audio/webm'
        elif filename.endswith('.opus'):
            mimetype = 'audio/opus'
        
        log.info(f"MIME类型: {mimetype}")
        log.info("✅ 开始传输音频文件")
        
        return send_file(
            file_path, 
            mimetype=mimetype,
            as_attachment=False,
            download_name=filename
        )
        
    except Exception as e:
        log.error(f"播放失败: {str(e)}")
        import traceback
        log.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'播放失败: {str(e)}'
        }), 500


@app.route('/api/file/<filename>')
def download_file(filename):
    """文件下载API"""
    try:
        return send_from_directory(
            app.config['DOWNLOAD_FOLDER'],
            filename,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        log.error(f"文件下载失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'文件下载失败: {str(e)}'
        }), 500


@app.route('/api/library', methods=['GET'])
@login_required_api
def get_library():
    """获取音乐库列表（当前用户）"""
    try:
        # 从数据库查询当前用户的音乐
        musics = Music.query.filter_by(user_id=current_user.id)\
            .order_by(Music.created_at.desc()).all()
        
        library = [music.to_dict() for music in musics]
        
        return jsonify({
            'success': True,
            'data': library,
            'total': len(library)
        })
        
    except Exception as e:
        log.error(f"获取音乐库失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取音乐库失败: {str(e)}'
        }), 500


@app.route('/api/delete/<int:music_id>', methods=['DELETE'])
@login_required_api
def delete_music(music_id):
    """删除音乐记录（只删除数据库记录）"""
    try:
        # 查找音乐记录
        music = Music.query.filter_by(id=music_id, user_id=current_user.id).first()
        
        if not music:
            return jsonify({
                'success': False,
                'message': '记录不存在或无权限删除'
            }), 404
        
        # 删除数据库记录
        db.session.delete(music)
        db.session.commit()
        
        log.info(f"已删除音乐记录: {music.title}")
        
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        log.error(f"删除失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }), 500


@app.route('/api/cleanup/<filename>', methods=['DELETE'])
@login_required_api
def cleanup_temp_file(filename):
    """清理临时音频文件（播放完毕后调用）"""
    try:
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            log.info(f"✅ 已清理临时文件: {filename}")
            return jsonify({
                'success': True,
                'message': '临时文件已清理'
            })
        else:
            return jsonify({
                'success': True,
                'message': '文件已不存在'
            })
    except Exception as e:
        log.error(f"清理文件失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'清理失败: {str(e)}'
        }), 500


@app.route('/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'service': 'Free Music Website'
    })


# 注册用户认证路由
from auth_routes import register_auth_routes
register_auth_routes(app)


if __name__ == '__main__':
    # 创建必要的目录
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)
    
    print("=" * 70)
    print("🎵 Free Music 免费在线音乐平台")
    print("=" * 70)
    print(f"访问地址: http://127.0.0.1:8080")
    print(f"下载目录: {app.config['DOWNLOAD_FOLDER']}")
    print(f"模式: 开发模式 (Debug=True)")
    print("\n提示：")
    print("  - 生产环境请使用 gunicorn: gunicorn -w 4 -b 0.0.0.0:8080 web_app:app")
    print("  - 或使用 waitress: waitress-serve --port=8080 web_app:app")
    print("=" * 70)
    
    # 启动Flask应用（开发模式）
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)

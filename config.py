# 应用配置
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# 文件路径配置
DOWNLOAD_FOLDER = './bilibili_music'
STATIC_FOLDER = './static'
TEMPLATE_FOLDER = './templates'

# 文件上传限
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB

# B站API配置
BILIBILI_API_BASE = 'https://api.bilibili.com'
SEARCH_MAX_RESULTS = 20

# 音频转换配置
AUDIO_BITRATE = '192k'
AUDIO_FORMAT = 'mp3'

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

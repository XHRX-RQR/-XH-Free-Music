#!/bin/bash

# ================================================================
# Free Music 生产环境启动脚本
# ================================================================

echo "======================================================================"
echo "🎵 Free Music - 免费在线音乐平台"
echo "======================================================================"
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

# 检查是否安装了依赖
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  未检测到依赖包，正在安装..."
    pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
fi

# 检查yt-dlp
if ! command -v yt-dlp &> /dev/null; then
    echo "⚠️  未检测到 yt-dlp，正在安装..."
    pip3 install yt-dlp -i https://mirrors.aliyun.com/pypi/simple/
fi

# 创建必要的目录
mkdir -p bilibili_music
mkdir -p static/css
mkdir -p static/js
mkdir -p templates

echo ""
echo "======================================================================"
echo "🚀 启动服务器"
echo "======================================================================"
echo ""
echo "访问地址: http://0.0.0.0:8080"
echo "进程数: 4"
echo "模式: 生产环境"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "======================================================================"
echo ""

# 使用 gunicorn 启动（推荐）
if command -v gunicorn &> /dev/null; then
    exec gunicorn \
        --bind 0.0.0.0:8080 \
        --workers 4 \
        --threads 2 \
        --timeout 120 \
        --access-logfile - \
        --error-logfile - \
        --log-level info \
        web_app:app
else
    echo "⚠️  未检测到 gunicorn，使用 waitress 启动..."
    
    # 使用 waitress 启动（备用方案）
    if python3 -c "import waitress" 2>/dev/null; then
        exec python3 -c "
from waitress import serve
from web_app import app
print('使用 waitress 启动服务器...')
serve(app, host='0.0.0.0', port=8080, threads=4)
"
    else
        echo "❌ 未找到 gunicorn 或 waitress"
        echo "请安装: pip3 install gunicorn"
        exit 1
    fi
fi

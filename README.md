# 🎵 XH Free Music - 永久免费的音乐流媒体平台

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Web-orange.svg)](https://github.com)
[![Free](https://img.shields.io/badge/Price-100%25%20Free-brightgreen.svg)](.)
[![Music Library](https://img.shields.io/badge/Music-Unlimited-ff69b4.svg)](.)

### 🌟 让音乐自由流动，让美好触手可及 🌟

**完全免费 · 海量曲库 · 无需付费 · 即搜即听**

[快速开始](#-快速开始) • [核心特性](#-核心特性) • [在线演示](#) • [贡献指南](#-贡献指南)

</div>

---

## 💎 为什么选择 XH Free Music？

在这个音乐付费墙林立的时代，我们相信**音乐应该是自由的，是触手可及的**。XH Free Music 致力于打造一个完全免费、无广告、无限制的音乐流媒体平台，让每个人都能享受音乐的美好。

### ✨ 核心优势

<table>
<tr>
<td width="50%">

#### 🆓 **100% 免费**
- ✅ 完全免费，无需付费会员
- ✅ 无广告干扰，纯净体验
- ✅ 无播放次数限制
- ✅ 无下载数量限制
- ✅ 所有功能永久免费开放

</td>
<td width="50%">

#### 🎼 **海量曲库**
- 🎵 涵盖华语、欧美、日韩、古典等各类音乐
- 🎤 支持主流歌手的完整专辑
- 🎸 包含小众独立音乐人作品
- 🎹 覆盖各类音乐风格和流派
- 📻 实时同步最新热门歌曲

</td>
</tr>
<tr>
<td width="50%">

#### ⚡ **即搜即听**
- 🔍 智能搜索，秒级响应
- 🎧 在线流媒体播放，无需等待
- 💾 支持离线下载，随时随地播放
- 📱 完美支持移动端和桌面端
- 🌐 无需VPN，国内外畅听无阻

</td>
<td width="50%">

#### 🛡️ **安全隐私**
- 🔐 数据加密存储，保护隐私
- 👤 多用户独立账号系统
- 🗂️ 个人专属音乐库
- 🚫 不追踪用户行为
- ✨ 开源透明，值得信赖

</td>
</tr>
</table>

---

## 📋 目录

- [为什么选择 XH Free Music](#-为什么选择-xh-free-music)
- [功能亮点](#-功能亮点)
- [快速开始](#-快速开始)
- [使用指南](#-使用指南)
- [技术架构](#-技术架构)
- [部署方案](#-部署方案)
- [常见问题](#-常见问题)
- [开发贡献](#-贡献指南)
- [许可协议](#-许可协议)

---

## 🎯 功能亮点

### 🎵 音乐播放

<table>
<tr>
<td>

**🔍 智能搜索**
- 支持歌手名 + 歌曲名精确搜索
- 支持专辑名、歌词关键词搜索
- 智能匹配算法，快速定位目标歌曲
- 实时搜索建议，提升搜索效率

**▶️ 在线播放**
- HTML5 原生播放器，兼容性强
- 流媒体技术，即点即播
- 支持进度拖拽、音量调节
- 自动续播，打造无缝听歌体验

**💾 离线下载**
- 一键下载高品质音频文件
- 支持 MP3、M4A 等主流格式
- 批量下载，高效便捷
- 下载记录管理，随时查看

</td>
<td>

**📚 个人曲库**
- 每个用户独立的音乐收藏空间
- 播放历史自动记录
- 播放次数统计
- 快速重播已听歌曲

**🎨 精美界面**
- 现代化深色主题，护眼舒适
- 流畅的动画效果和过渡
- 渐变色彩设计，视觉享受
- 响应式布局，完美适配各端设备

**🔐 账号系统**
- 安全的用户注册与登录
- 密码加密存储，保护隐私
- 多用户数据完全隔离
- 会话管理，自动登录

</td>
</tr>
</table>

### 🌈 使用场景

- **🎧 日常听歌**：无广告干扰，沉浸式音乐体验
- **💼 办公学习**：背景音乐助力，提升专注力和效率
- **🏃 运动健身**：动感节奏相伴，激发运动热情
- **😴 睡前放松**：轻柔旋律陪伴，舒缓身心助眠
- **🎉 派对聚会**：海量曲库支持，随心所欲点歌

---

## 🏗️ 技术架构

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.9+ | 核心开发语言 |
| **Flask** | 3.0+ | Web框架 |
| **Flask-SQLAlchemy** | 3.0+ | ORM数据库 |
| **Flask-Login** | 0.6+ | 用户认证 |
| **yt-dlp** | 2024.8+ | 音频资源获取 |
| **asyncio** | 内置 | 异步任务处理 |

### 前端技术栈

| 技术 | 用途 |
|------|------|
| **HTML5** | 语义化结构 |
| **CSS3** | 现代样式、动画、渐变 |
| **JavaScript (ES6+)** | 交互逻辑、异步请求 |
| **Fetch API** | RESTful API 调用 |
| **Audio API** | 音频播放控制 |

### 数据库设计

```sql
-- 用户表
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 音乐表
CREATE TABLE musics (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    artist VARCHAR(200),
    filename VARCHAR(255) NOT NULL,
    file_size INTEGER,
    video_url VARCHAR(500),
    play_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                      客户端 (Browser)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  HTML/CSS   │  │ JavaScript  │  │  Audio API  │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
└─────────┼─────────────────┼─────────────────┼───────────┘
          │                 │                 │
          │      HTTP/JSON  │    WebSocket    │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────┐
│                  Flask Web 服务器                        │
│  ┌──────────────────────────────────────────────────┐   │
│  │              路由层 (Routes)                     │   │
│  │  /login  /register  /api/search  /api/cache    │   │
│  └────────────────┬─────────────────────────────────┘   │
│                   │                                      │
│  ┌────────────────▼─────────────────┐                   │
│  │        业务逻辑层 (Services)      │                   │
│  │  - 用户认证  - 音乐搜索          │                   │
│  │  - 音频下载  - 缓存管理          │                   │
│  └────────────────┬─────────────────┘                   │
│                   │                                      │
│  ┌────────────────▼─────────────────┐                   │
│  │      数据访问层 (Models)          │                   │
│  │  User Model  │  Music Model      │                   │
│  └────────────────┬─────────────────┘                   │
└───────────────────┼──────────────────────────────────────┘
                    │
          ┌─────────▼─────────┐
          │   SQLite 数据库    │
          │  - users 表       │
          │  - musics 表      │
          └───────────────────┘
```

---

## 💻 系统要求

### 最低配置
- **操作系统**：Linux / macOS / Windows 10+
- **Python**：3.9 或更高版本
- **内存**：512MB RAM
- **磁盘空间**：500MB（不含音乐文件）
- **网络**：稳定的互联网连接

### 推荐配置
- **操作系统**：Ubuntu 20.04+ / macOS 12+
- **Python**：3.10+
- **内存**：2GB RAM
- **磁盘空间**：10GB SSD
- **网络**：10Mbps+ 带宽

---

## 🚀 快速开始

### 1️⃣ 克隆项目



下载本项目根目录。

### 2️⃣ 安装依赖

推荐使用虚拟环境：

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

**国内镜像加速**：
```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 3️⃣ 初始化数据库

```bash
python3 init_db.py
```

**输出示例**：
```
======================================================================
🗄️  数据库初始化
======================================================================
✅ 创建数据库表...
📊 数据库表结构:
  - users: 用户表
  - musics: 音乐表
👤 创建测试用户...
  ✅ 测试用户创建成功: test / 123456
======================================================================
✅ 数据库初始化完成！
======================================================================
```

### 4️⃣ 启动服务

**开发模式**：
```bash
python3 web_app.py
```

**生产模式**（推荐）：
```bash
# 使用 Gunicorn (Linux/macOS)
gunicorn -w 4 -b 0.0.0.0:8080 web_app:app

# 使用 Waitress (跨平台)
waitress-serve --port=8080 web_app:app
```

## 5️⃣ 访问应用

在浏览器中打开：
- **本地访问**：http://127.0.0.1:8080
- **局域网访问**：http://YOUR_IP:8080

**默认测试账号**：
- 用户名：`test`
- 密码：`123456`

> 💡 **提示**：首次使用建议注册个人账号，享受专属音乐库

---

## 📱 使用指南

### 注册与登录

1. **注册新账号**
   - 点击"注册"按钮
   - 填写用户名、邮箱和密码
   - 提交完成注册

2. **登录账号**
   - 输入用户名和密码
   - 点击"登录"按钮
   - 自动跳转到主界面

### 搜索与播放音乐

1. **搜索歌曲**
   ```
   🎵 搜索页面
   ├─ 输入歌手名：周杰伦
   ├─ 输入歌曲名：晴天
   └─ 点击搜索按钮
   ```

2. **播放音乐**
   - 在搜索结果中点击"播放"按钮
   - 系统自动获取音频并开始播放
   - 底部播放器显示当前播放信息

3. **控制播放**
   - ⏸️ **暂停/播放**：点击播放器中央按钮
   - ⏮️ **上一曲**：点击左侧箭头
   - ⏭️ **下一曲**：点击右侧箭头
   - 🔊 **音量调节**：拖动音量滑块
   - 📊 **进度调整**：拖动进度条

### 管理个人曲库

1. **查看曲库**
   - 切换到"我的曲库"标签
   - 查看所有播放过的歌曲记录

2. **重新播放**
   - 点击曲库中任意歌曲的"播放"按钮
   - 系统重新获取并播放

3. **删除记录**
   - 点击歌曲旁的"删除"按钮
   - 确认后从曲库中移除

### 下载音乐

1. **下载当前播放**
   - 在播放器中点击"下载"按钮
   - 音频文件自动保存到本地

2. **批量下载**
   - 在搜索结果中逐个下载
   - 支持多首歌曲连续下载

---

## 📁 项目结构

```
CUI/
├── web_app.py              # Flask 主应用入口
├── models.py               # 数据库模型定义
├── auth_routes.py          # 用户认证路由
├── music_service.py        # 音乐服务核心逻辑
├── init_db.py             # 数据库初始化脚本
├── requirements.txt        # Python 依赖清单
├── freemusic.db           # SQLite 数据库文件
│
├── templates/             # HTML 模板目录
│   ├── index.html         # 主页面
│   ├── login.html         # 登录页面
│   ├── register.html      # 注册页面
│   └── test.html          # 测试页面
│
├── static/                # 静态资源目录
│   ├── css/
│   │   └── style.css      # 全局样式表 (1084行)
│   └── js/
│       └── app.js         # 前端交互逻辑 (795行)
│
└── bilibili_music/        # 音乐文件存储目录
    └── [用户名]_[歌手]-[歌曲].m4a
```

---

## ⚙️ 配置说明

### 环境变量配置

创建 `.env` 文件（可选）：

```bash
# Flask 配置
FLASK_APP=web_app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# 数据库配置
DATABASE_URI=sqlite:///freemusic.db

# 服务器配置
HOST=0.0.0.0
PORT=8080

# 文件存储
DOWNLOAD_FOLDER=./bilibili_music
MAX_CONTENT_LENGTH=524288000  # 500MB
```

### Web_app.py 配置项

```python
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///freemusic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 最大上传500MB
app.config['DOWNLOAD_FOLDER'] = './bilibili_music'
```

---

## 📡 API文档

### 🔐 认证相关

#### 注册用户
```http
POST /api/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**响应**：
```json
{
  "success": true,
  "message": "注册成功！请登录"
}
```

#### 用户登录
```http
POST /api/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

**响应**：
```json
{
  "success": true,
  "message": "登录成功！",
  "data": {
    "username": "test",
    "email": "test@example.com"
  }
}
```

#### 用户登出
```http
POST /api/logout
```

#### 获取当前用户信息
```http
GET /api/user/info
```

**响应**：
```json
{
  "success": true,
  "is_authenticated": true,
  "data": {
    "id": 1,
    "username": "test",
    "email": "test@example.com"
  }
}
```

### 🎵 音乐相关

#### 搜索音乐
```http
POST /api/search
Content-Type: application/json
Authorization: Required (登录后)

{
  "keyword": "周杰伦 晴天"
}
```

**响应**：
```json
{
  "success": true,
  "data": [
    {
      "title": "晴天 - 周杰伦",
      "url": "https://www.bilibili.com/video/BV...",
      "score": 85,
      "bvid": "BV1d4411N7zD"
    }
  ],
  "total": 1
}
```

#### 缓存音乐到服务器
```http
POST /api/cache
Content-Type: application/json
Authorization: Required

{
  "video_url": "https://www.bilibili.com/video/BV...",
  "title": "晴天",
  "artist": "周杰伦",
  "bvid": "BV1d4411N7zD"
}
```

**响应**：
```json
{
  "success": true,
  "message": "缓存成功",
  "data": {
    "id": 1,
    "title": "晴天",
    "artist": "周杰伦",
    "filename": "test_周杰伦 - 晴天.m4a",
    "file_size": 6717560,
    "play_url": "/api/stream/test_周杰伦 - 晴天.m4a",
    "download_url": "/api/file/test_周杰伦 - 晴天.m4a"
  }
}
```

#### 获取音乐库列表
```http
GET /api/library
Authorization: Required
```

**响应**：
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "晴天",
      "artist": "周杰伦",
      "filename": "test_周杰伦 - 晴天.m4a",
      "play_count": 5,
      "created_at": "2025-12-13T19:00:00"
    }
  ],
  "total": 1
}
```

#### 流式播放音乐
```http
GET /api/stream/:filename
Authorization: Required
```

#### 下载音乐文件
```http
GET /api/file/:filename
Authorization: Required
```

#### 删除音乐
```http
DELETE /api/delete/:music_id
Authorization: Required
```

---

## 🛠️ 开发指南

### 本地开发环境搭建

1. **安装开发工具**：
```bash
pip install pytest pytest-cov black flake8
```

2. **代码格式化**：
```bash
black web_app.py models.py
```

3. **代码检查**：
```bash
flake8 web_app.py --max-line-length=120
```

### 调试模式

启用 Flask 调试模式：
```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

查看详细日志：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 数据库迁移

使用 Flask-Migrate（可选）：
```bash
pip install flask-migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 🚢 部署方案

### Docker 部署（推荐）

1. **创建 Dockerfile**：
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python3 init_db.py

EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "web_app:app"]
```

2. **构建镜像**：
```bash
docker build -t freemusic:latest .
```

3. **运行容器**：
```bash
docker run -d -p 8080:8080 \
  -v $(pwd)/bilibili_music:/app/bilibili_music \
  -v $(pwd)/freemusic.db:/app/freemusic.db \
  --name freemusic \
  freemusic:latest
```

### Nginx 反向代理

**nginx.conf**：
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/freemusic/CUI/static;
        expires 30d;
    }
}
```

### Systemd 服务

**freemusic.service**：
```ini
[Unit]
Description=Free Music Web Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/freemusic/CUI
ExecStart=/usr/bin/gunicorn -w 4 -b 0.0.0.0:8080 web_app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl enable freemusic
sudo systemctl start freemusic
```

---

## ❓ 常见问题

### Q1: 无法下载音乐？
**A**: 确保已安装 `ffmpeg`：
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# 下载 https://ffmpeg.org/download.html
```

### Q2: 数据库被锁定？
**A**: SQLite 不支持高并发写入，生产环境建议使用 PostgreSQL：
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/xhfreemusic'
```

### Q3: 音频无法播放？
**A**: 检查浏览器控制台错误，确认：
- 文件路径正确
- MIME 类型正确（audio/mp4, audio/mpeg）
- CORS 配置正确

### Q4: 如何修改端口？
**A**: 编辑 `web_app.py` 最后一行：
```python
app.run(host='0.0.0.0', port=YOUR_PORT, debug=True)
```

### Q5: 如何清空数据库？
**A**: 重新运行初始化脚本：
```bash
python3 init_db.py
```

---

## 📄 许可协议

本项目采用 [MIT License](LICENSE) 开源协议。

```
MIT License

Copyright (c) 2025 Free Music

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🤝 贡献指南

我们热烈欢迎所有形式的贡献！无论是报告Bug、提出新功能建议，还是提交代码改进，都能让XH Free Music变得更好。

### 如何贡献

1. **🐛 报告问题**
   - 在 [Issues](https://github.com/XHRX-RQR/-XH-Free-Music/issues) 中创建新issue
   - 详细描述问题场景和复现步骤
   - 附上错误截图或日志

2. **💡 提出建议**
   - 在 Issues 中提出功能需求
   - 说明该功能的使用场景和价值

3. **📝 贡献代码**
   - Fork 本仓库
   - 创建特性分支 (`git checkout -b feature/AmazingFeature`)
   - 编写代码并测试
   - 提交更改 (`git commit -m 'Add some AmazingFeature'`)
   - 推送到分支 (`git push origin feature/AmazingFeature`)
   - 开启 Pull Request

### 贡献规范

- 代码风格遵循 PEP 8 规范
- 提交信息使用清晰的中文或英文描述
- 添加必要的注释和文档
- 确保不破坏现有功能

---

## 📧 联系方式

- **项目主页**：https://github.com/XHRX-RQR/-XH-Free-Music
- **邮箱**：wjxhmax@outlook.com
- **社区讨论**：欢迎加入我们的讨论组

---

## 🙏 致谢

感谢以下开源项目为 XH Free Music 提供的支持：

- [Flask](https://flask.palletsprojects.com/) - 优雅的 Python Web 框架
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 强大的媒体处理工具
- [SQLAlchemy](https://www.sqlalchemy.org/) - 完善的 Python ORM 框架
- 所有开源社区的贡献者们

特别感谢所有支持和使用 XH Free Music 的用户，是你们让音乐更加自由！

---

## ⚠️ 免责声明

XH Free Music 是一个开源学习项目，旨在技术交流和学习使用。

- 本项目仅供个人学习和研究使用
- 用户应遵守所在地区的法律法规和版权规定
- 请勿将本项目用于任何商业用途
- 因使用本项目产生的任何纠纷，开发者不承担任何责任

如果您喜欢某位艺术家的作品，请通过正规渠道支持他们。

---

<div align="center">

### 🌟 让音乐自由流动 🌟

**XH Free Music** - 永久免费的音乐流媒体平台

Made with ❤️ by XH Free Music Team

---

如果这个项目对你有帮助，请给我们一个 ⭐ Star！

您的支持是我们持续改进的动力

[⬆️ 回到顶部](#-xh-free-music---永久免费的音乐流媒体平台)

</div>

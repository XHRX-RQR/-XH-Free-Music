"""
数据库模型
定义用户表和音乐表
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系：一个用户有多首音乐
    musics = db.relationship('Music', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """设置密码（加密）"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Music(db.Model):
    """音乐模型（只存储元数据，不存储音频文件）"""
    __tablename__ = 'musics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # 音乐基本信息
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200))
    
    # B站相关信息
    video_url = db.Column(db.String(500), nullable=False)  # B站视频链接
    bvid = db.Column(db.String(50))
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    played_at = db.Column(db.DateTime)  # 最后播放时间
    play_count = db.Column(db.Integer, default=0)  # 播放次数
    
    def __repr__(self):
        return f'<Music {self.title} by {self.artist}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'video_url': self.video_url,
            'bvid': self.bvid,
            'play_count': self.play_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'played_at': self.played_at.isoformat() if self.played_at else None,
        }

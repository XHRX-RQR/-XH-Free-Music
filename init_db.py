#!/usr/bin/env python3
"""
数据库初始化脚本
清除旧数据并创建新的数据库表
"""
import os
import shutil
from flask import Flask
from models import db, User, Music

def init_database():
    """初始化数据库"""
    print("="*70)
    print("🗄️  数据库初始化")
    print("="*70)
    
    # 创建Flask应用
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///freemusic.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # 删除旧数据库
        db_file = 'freemusic.db'
        if os.path.exists(db_file):
            print(f"❌ 删除旧数据库: {db_file}")
            os.remove(db_file)
        
        # 清空音乐文件目录
        music_dir = './bilibili_music'
        if os.path.exists(music_dir):
            print(f"❌ 清空音乐目录: {music_dir}")
            shutil.rmtree(music_dir)
            os.makedirs(music_dir)
        else:
            os.makedirs(music_dir)
        
        # 创建所有表
        print("✅ 创建数据库表...")
        db.create_all()
        
        print("\n📊 数据库表结构:")
        print("  - users: 用户表")
        print("  - musics: 音乐表")
        
        # 创建测试用户（可选）
        print("\n👤 创建测试用户...")
        test_user = User(username='test', email='test@example.com')
        test_user.set_password('123456')
        db.session.add(test_user)
        db.session.commit()
        print(f"  ✅ 测试用户创建成功: test / 123456")
        
        print("\n" + "="*70)
        print("✅ 数据库初始化完成！")
        print("="*70)
        print("\n提示：")
        print("  - 数据库文件: freemusic.db")
        print("  - 音乐目录: ./bilibili_music/")
        print("  - 测试账号: test / 123456")
        print()

if __name__ == '__main__':
    init_database()

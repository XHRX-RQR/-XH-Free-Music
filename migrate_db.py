#!/usr/bin/env python3
"""
数据库迁移脚本
删除旧的 filename 和 file_size 字段，清空音乐记录
"""
import os
import sys
from web_app import app, db
from models import Music

def migrate_database():
    """迁移数据库"""
    with app.app_context():
        print("=" * 70)
        print("🔄 数据库迁移")
        print("=" * 70)
        
        try:
            # 删除所有音乐记录
            print("📊 清空音乐记录...")
            Music.query.delete()
            db.session.commit()
            print("✅ 音乐记录已清空")
            
            # 删除所有音频文件
            print("📁 清理音频文件...")
            download_folder = app.config['DOWNLOAD_FOLDER']
            if os.path.exists(download_folder):
                for filename in os.listdir(download_folder):
                    if filename.endswith(('.m4a', '.mp3', '.webm')):
                        file_path = os.path.join(download_folder, filename)
                        os.remove(file_path)
                        print(f"  ✓ 删除: {filename}")
            print("✅ 音频文件已清理")
            
            # 重新创建表结构（自动适配新模型）
            print("🔨 更新表结构...")
            db.drop_all()
            db.create_all()
            print("✅ 表结构已更新")
            
            print("=" * 70)
            print("✅ 数据库迁移完成！")
            print("=" * 70)
            print("\n说明：")
            print("  - 音乐记录不再存储文件名和文件大小")
            print("  - 播放时临时下载，播放结束后自动删除")
            print("  - 大幅节省服务器存储空间")
            print("=" * 70)
            
        except Exception as e:
            print(f"❌ 迁移失败: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    migrate_database()


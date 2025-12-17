# 用户认证相关路由
from flask import request, jsonify, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user
from models import db, User

def register_auth_routes(app):
    """注册认证相关路由"""
    
    @app.route('/login')
    def login():
        """登录页面"""
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('login.html')
    
    
    @app.route('/register')
    def register():
        """注册页面"""
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('register.html')
    
    
    @app.route('/api/register', methods=['POST'])
    def api_register():
        """注册API"""
        try:
            data = request.get_json()
            username = data.get('username', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            
            # 验证输入
            if not username or not email or not password:
                return jsonify({
                    'success': False,
                    'message': '用户名、邮箱和密码不能为空'
                }), 400
            
            if len(username) < 3 or len(username) > 20:
                return jsonify({
                    'success': False,
                    'message': '用户名长度必须在3-20个字符之间'
                }), 400
            
            if len(password) < 6:
                return jsonify({
                    'success': False,
                    'message': '密码长度至少6个字符'
                }), 400
            
            # 检查用户名是否已存在
            if User.query.filter_by(username=username).first():
                return jsonify({
                    'success': False,
                    'message': '用户名已存在'
                }), 400
            
            # 检查邮箱是否已存在
            if User.query.filter_by(email=email).first():
                return jsonify({
                    'success': False,
                    'message': '邮箱已被注册'
                }), 400
            
            # 创建新用户
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': '注册成功！请登录'
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'注册失败: {str(e)}'
            }), 500
    
    
    @app.route('/api/login', methods=['POST'])
    def api_login():
        """登录API"""
        try:
            data = request.get_json()
            username = data.get('username', '').strip()
            password = data.get('password', '')
            
            if not username or not password:
                return jsonify({
                    'success': False,
                    'message': '用户名和密码不能为空'
                }), 400
            
            # 查找用户
            user = User.query.filter_by(username=username).first()
            
            if not user or not user.check_password(password):
                return jsonify({
                    'success': False,
                    'message': '用户名或密码错误'
                }), 401
            
            # 登录用户
            login_user(user, remember=True)
            
            return jsonify({
                'success': True,
                'message': '登录成功！',
                'data': {
                    'username': user.username,
                    'email': user.email
                }
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'登录失败: {str(e)}'
            }), 500
    
    
    @app.route('/api/logout', methods=['POST'])
    def api_logout():
        """登出API"""
        logout_user()
        return jsonify({
            'success': True,
            'message': '已退出登录'
        })
    
    
    @app.route('/api/user/info')
    def api_user_info():
        """获取当前用户信息"""
        if not current_user.is_authenticated:
            return jsonify({
                'success': False,
                'message': '未登录',
                'is_authenticated': False
            })
        
        return jsonify({
            'success': True,
            'is_authenticated': True,
            'data': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email
            }
        })

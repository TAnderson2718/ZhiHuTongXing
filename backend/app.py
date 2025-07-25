"""
智护童行 - Flask后端应用 (重构版)
"""
from flask import Flask, send_from_directory, render_template
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user
import os
from config import config
from models import init_database, insert_default_content, AdminUser
from routes import register_routes

def create_app(test_config=None):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 配置应用
    if test_config is None:
        # 生产配置
        app.secret_key = config.SECRET_KEY
        app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
        app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
        app.config['DATABASE_PATH'] = config.DATABASE_PATH
        
        # 会话安全配置
        app.config['SESSION_COOKIE_SECURE'] = False  # 开发环境设为False，生产环境应设为True
        app.config['SESSION_COOKIE_HTTPONLY'] = True  # 防止XSS攻击
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF保护
        app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 会话超时时间（30分钟）
        app.config['REMEMBER_COOKIE_DURATION'] = 86400  # 记住我功能持续时间（24小时）
    else:
        # 测试配置
        app.config.update(test_config)
        if 'SECRET_KEY' not in test_config:
            app.secret_key = config.SECRET_KEY
        if 'UPLOAD_FOLDER' not in test_config:
            app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
        if 'MAX_CONTENT_LENGTH' not in test_config:
            app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    
    # 启用CORS以支持前后端分离
    CORS(app, supports_credentials=True, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])
    
    # 启用CSRF保护
    csrf = CSRFProtect(app)
    
    # 配置Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin_dashboard'
    login_manager.login_message = '请先登录以访问此页面'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Flask-Login用户加载回调函数"""
        return AdminUser.get_by_id(user_id, app.config.get('DATABASE_PATH'))
    
    # 注册路由
    register_routes(app, csrf)
    
    # 静态文件服务
    @app.route('/static/uploads/<filename>')
    def uploaded_file(filename):
        """提供上传的文件"""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # 根路径显示前端用户页面
    @app.route('/')
    def index():
        """前端用户页面"""
        return send_from_directory('../', 'index.html')
    
    # 管理后台页面
    @app.route('/admin')
    def admin_dashboard():
        """管理后台首页"""
        # 如果用户未登录，传递None；如果已登录，传递用户信息
        user_data = None
        if current_user.is_authenticated:
            user_data = {
                'id': current_user.id,
                'username': current_user.username
            }
        return render_template('admin_basic.html', currentUser=user_data)
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return {
            'success': False,
            'error': '接口不存在'
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {
            'success': False,
            'error': '服务器内部错误'
        }, 500
    
    return app

def init_app():
    """初始化应用数据"""
    # 初始化数据库
    init_database()
    insert_default_content()
    AdminUser.create_default_admin()

if __name__ == '__main__':
    # 创建应用实例
    app = create_app()
    
    # 初始化数据
    init_app()
    
    print("智护童行后端服务启动中...")
    print(f"管理后台地址: http://{config.HOST}:{config.PORT}/admin")
    print("默认管理员账户: admin / admin123")
    print("注意：生产环境请修改默认密码并设置环境变量！")
    
    # 启动应用
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)

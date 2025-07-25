"""
路由模块初始化
"""
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .api import api_bp
from .admin import admin_bp

def register_routes(app: Flask, csrf: CSRFProtect):
    """注册所有路由"""
    
    # 为公共API豁免CSRF保护
    csrf.exempt(api_bp)
    
    # 注册蓝图
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    
    return app

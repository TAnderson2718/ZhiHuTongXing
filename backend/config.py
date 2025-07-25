"""
配置管理模块
"""
import os
from dataclasses import dataclass

@dataclass
class Config:
    """应用配置类"""
    
    # 安全配置
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # 数据库配置
    DATABASE_PATH: str = os.getenv('DATABASE_PATH', os.path.join(os.path.dirname(__file__), 'zhihu_tongxing.db'))
    
    # 文件上传配置
    UPLOAD_FOLDER: str = os.getenv('UPLOAD_FOLDER', os.path.join(os.path.dirname(__file__), 'static', 'uploads'))
    MAX_CONTENT_LENGTH: int = int(os.getenv('MAX_CONTENT_LENGTH', 100 * 1024 * 1024))  # 100MB
    
    # 服务器配置
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', 5001))
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # 允许的文件扩展名
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'}
    
    # 允许的MIME类型（用于文件内容验证）
    ALLOWED_IMAGE_MIMES = {
        'image/png', 'image/jpeg', 'image/gif', 
        'image/svg+xml', 'image/webp'
    }
    ALLOWED_VIDEO_MIMES = {
        'video/mp4', 'video/avi', 'video/quicktime',
        'video/x-msvideo', 'video/x-flv', 'video/webm'
    }

# 创建配置实例
config = Config()

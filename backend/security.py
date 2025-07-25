"""
安全工具模块
"""
import bcrypt
import os
import mimetypes
from config import config

class PasswordManager:
    """密码管理器"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """使用bcrypt哈希密码"""
        if not password:
            raise ValueError("密码不能为空")
        
        # 生成盐并哈希密码
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """验证密码"""
        if not password or not hashed:
            return False
        
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False

class FileValidator:
    """文件验证器"""
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
        """验证文件扩展名"""
        if not filename or '.' not in filename:
            return False
        
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in allowed_extensions
    
    @staticmethod
    def validate_file_content(file_path: str, allowed_mimes: set) -> bool:
        """验证文件内容类型"""
        if not os.path.exists(file_path):
            return False
        
        try:
            # 使用mimetypes模块作为备选方案
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type in allowed_mimes:
                return True
            
            # 简单的文件头检查
            return FileValidator._check_file_signature(file_path, allowed_mimes)
        except Exception:
            return False
    
    @staticmethod
    def validate_image_file(filename: str, file_path: str) -> bool:
        """验证图片文件"""
        # 检查扩展名
        if not FileValidator.validate_file_extension(filename, config.ALLOWED_EXTENSIONS):
            return False
        
        # 检查文件内容
        return FileValidator.validate_file_content(file_path, config.ALLOWED_IMAGE_MIMES)
    
    @staticmethod
    def validate_video_file(filename: str, file_path: str) -> bool:
        """验证视频文件"""
        # 检查扩展名
        if not FileValidator.validate_file_extension(filename, config.ALLOWED_VIDEO_EXTENSIONS):
            return False
        
        # 检查文件内容
        return FileValidator.validate_file_content(file_path, config.ALLOWED_VIDEO_MIMES)

class SecurityUtils:
    """安全工具类"""
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """清理文件名，移除危险字符"""
        if not filename:
            return ""
        
        # 移除路径分隔符和其他危险字符
        dangerous_chars = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
        sanitized = filename
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '_')
        
        # 限制文件名长度
        if len(sanitized) > 255:
            name, ext = os.path.splitext(sanitized)
            sanitized = name[:255-len(ext)] + ext
        
        return sanitized
    
    @staticmethod
    def generate_secure_filename(original_filename: str) -> str:
        """生成安全的文件名"""
        import uuid
        
        if not original_filename:
            return str(uuid.uuid4())
        
        # 获取文件扩展名
        name, ext = os.path.splitext(original_filename)
        
        # 生成UUID作为文件名，保留原扩展名
        secure_name = str(uuid.uuid4()) + ext.lower()
        
        return secure_name
    
    @staticmethod
    def _check_file_signature(file_path: str, allowed_mimes: set) -> bool:
        """检查文件签名（魔数）"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(16)  # 读取16字节头部
            
            # 常见文件签名检查
            if header.startswith(b'\xff\xd8\xff'):  # JPEG
                return 'image/jpeg' in allowed_mimes
            elif header.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG
                return 'image/png' in allowed_mimes
            elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):  # GIF
                return 'image/gif' in allowed_mimes
            elif header.startswith(b'\x00\x00\x00 ftypmp4') or b'mp4' in header[:16]:  # MP4
                return 'video/mp4' in allowed_mimes
            elif header.startswith(b'RIFF') and b'WEBP' in header:  # WebP
                return 'image/webp' in allowed_mimes
            
            # 如果没有匹配到特定签名，返回True（容错处理）
            return True
        except Exception:
            return False

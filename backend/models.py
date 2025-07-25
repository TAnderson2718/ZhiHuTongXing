"""
数据库模型定义
"""
import sqlite3
import os
from datetime import datetime
from flask_login import UserMixin
from config import config
from security import PasswordManager

def init_database(db_path=None):
    """初始化数据库和表结构"""
    if db_path is None:
        db_path = config.DATABASE_PATH
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建text_content表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS text_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            element_key TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建image_content表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS image_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_key TEXT UNIQUE NOT NULL,
            file_path TEXT NOT NULL,
            original_filename TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建video_content表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS video_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_key TEXT UNIQUE NOT NULL,
            file_path TEXT NOT NULL,
            original_filename TEXT,
            title TEXT,
            description TEXT,
            duration INTEGER,
            file_size INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建管理员表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection(db_path=None):
    """获取数据库连接"""
    try:
        if db_path is None:
            db_path = config.DATABASE_PATH
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # 使查询结果可以像字典一样访问
        return conn
    except sqlite3.Error as e:
        raise Exception(f"数据库连接失败: {str(e)}")

def insert_default_content():
    """插入默认内容数据"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 默认文本内容
    default_texts = [
        ('main_title', '智护童行'),
        ('main_subtitle', '专业的家庭照护教育平台'),
        ('main_description', '从自我评估到专业学习，我们为您提供一站式家庭照护解决方案'),
        ('halls_title', '探索五大核心功能展馆'),
        ('halls_description', '从自我评估到专业学习，我们为您提供一站式家庭照护解决方案。'),
        ('assessment_title', '自我评估'),
        ('assessment_description', '了解您当前的照护知识水平'),
        ('knowledge_title', '知识学习'),
        ('knowledge_description', '系统学习专业照护知识'),
        ('experience_title', '体验互动'),
        ('experience_description', '通过游戏化学习提升技能'),
        ('support_title', '成长对策室'),
        ('support_description', '测评反馈、个性化干预、成长奖励'),
        ('archive_title', '个人档案'),
        ('archive_description', '记录您的学习历程'),
        ('wechat_info', '微信号: zhihutongxing')
    ]
    
    # 默认图片内容
    default_images = [
        ('hero_banner', '/static/uploads/hero-banner.jpg'),
        ('assessment_icon', '/static/uploads/assessment-icon.svg'),
        ('knowledge_icon', '/static/uploads/knowledge-icon.svg'),
        ('experience_icon', '/static/uploads/experience-icon.svg'),
        ('support_icon', '/static/uploads/support-icon.svg'),
        ('archive_icon', '/static/uploads/archive-icon.svg')
    ]
    
    # 默认视频内容
    default_videos = [
        ('newborn_care_intro', '/static/uploads/newborn-care-intro.mp4', '新生儿护理基础介绍', '学习新生儿护理的基本知识和技能'),
        ('feeding_techniques', '/static/uploads/feeding-techniques.mp4', '婴幼儿喂养技巧', '掌握科学的婴幼儿喂养方法'),
        ('safety_tips', '/static/uploads/safety-tips.mp4', '儿童安全防护要点', '了解家庭环境中的安全防护措施')
    ]
    
    # 插入文本内容（如果不存在）
    for element_key, content in default_texts:
        cursor.execute('''
            INSERT OR IGNORE INTO text_content (element_key, content)
            VALUES (?, ?)
        ''', (element_key, content))
    
    # 插入图片内容（如果不存在）
    for image_key, file_path in default_images:
        cursor.execute('''
            INSERT OR IGNORE INTO image_content (image_key, file_path, original_filename)
            VALUES (?, ?, ?)
        ''', (image_key, file_path, f'{image_key}.jpg'))
    
    # 插入视频内容（如果不存在）
    for video_key, file_path, title, description in default_videos:
        cursor.execute('''
            INSERT OR IGNORE INTO video_content (video_key, file_path, title, description, original_filename)
            VALUES (?, ?, ?, ?, ?)
        ''', (video_key, file_path, title, description, f'{video_key}.mp4'))
    
    conn.commit()
    conn.close()

class TextContent:
    """文本内容模型"""
    
    @staticmethod
    def get_all():
        """获取所有文本内容"""
        conn = get_db_connection()
        texts = conn.execute('SELECT * FROM text_content ORDER BY element_key').fetchall()
        conn.close()
        return [dict(text) for text in texts]
    
    @staticmethod
    def get_by_key(element_key):
        """根据element_key获取文本内容"""
        conn = get_db_connection()
        text = conn.execute(
            'SELECT * FROM text_content WHERE element_key = ?', 
            (element_key,)
        ).fetchone()
        conn.close()
        return dict(text) if text else None
    
    @staticmethod
    def update(element_key, content):
        """更新文本内容"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE text_content 
            SET content = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE element_key = ?
        ''', (content, element_key))
        
        # 如果记录不存在，则插入新记录
        if cursor.rowcount == 0:
            cursor.execute('''
                INSERT INTO text_content (element_key, content)
                VALUES (?, ?)
            ''', (element_key, content))
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0

class ImageContent:
    """图片内容模型"""
    
    @staticmethod
    def get_all():
        """获取所有图片内容"""
        conn = get_db_connection()
        images = conn.execute('SELECT * FROM image_content ORDER BY image_key').fetchall()
        conn.close()
        return [dict(image) for image in images]
    
    @staticmethod
    def get_by_key(image_key):
        """根据image_key获取图片内容"""
        conn = get_db_connection()
        image = conn.execute(
            'SELECT * FROM image_content WHERE image_key = ?', 
            (image_key,)
        ).fetchone()
        conn.close()
        return dict(image) if image else None
    
    @staticmethod
    def update(image_key, file_path, original_filename=None):
        """更新图片内容"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE image_content 
            SET file_path = ?, original_filename = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE image_key = ?
        ''', (file_path, original_filename, image_key))
        
        # 如果记录不存在，则插入新记录
        if cursor.rowcount == 0:
            cursor.execute('''
                INSERT INTO image_content (image_key, file_path, original_filename)
                VALUES (?, ?, ?)
            ''', (image_key, file_path, original_filename))
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0

class VideoContent:
    """视频内容模型"""
    
    @staticmethod
    def get_all():
        """获取所有视频内容"""
        conn = get_db_connection()
        videos = conn.execute('SELECT * FROM video_content ORDER BY video_key').fetchall()
        conn.close()
        return [dict(video) for video in videos]
    
    @staticmethod
    def get_by_key(video_key):
        """根据video_key获取视频内容"""
        conn = get_db_connection()
        video = conn.execute(
            'SELECT * FROM video_content WHERE video_key = ?', 
            (video_key,)
        ).fetchone()
        conn.close()
        return dict(video) if video else None
    
    @staticmethod
    def update(video_key, file_path, original_filename=None, title=None, description=None, duration=None, file_size=None):
        """更新视频内容"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE video_content 
            SET file_path = ?, original_filename = ?, title = ?, description = ?, 
                duration = ?, file_size = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE video_key = ?
        ''', (file_path, original_filename, title, description, duration, file_size, video_key))
        
        # 如果记录不存在，则插入新记录
        if cursor.rowcount == 0:
            cursor.execute('''
                INSERT INTO video_content (video_key, file_path, original_filename, title, description, duration, file_size)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (video_key, file_path, original_filename, title, description, duration, file_size))
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def delete(video_key):
        """删除视频内容"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM video_content WHERE video_key = ?', (video_key,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0

class AdminUser(UserMixin):
    """管理员用户模型 - 兼容 Flask-Login"""
    
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
    
    def get_id(self):
        """Flask-Login 要求的方法：返回用户唯一标识"""
        return str(self.id)
    
    @property
    def is_authenticated(self):
        """Flask-Login 要求的属性：用户是否已认证"""
        return True
    
    @property
    def is_active(self):
        """Flask-Login 要求的属性：用户是否活跃"""
        return True
    
    @property
    def is_anonymous(self):
        """Flask-Login 要求的属性：用户是否匿名"""
        return False
    
    @staticmethod
    def get_by_id(user_id, db_path=None):
        """根据用户ID获取用户对象"""
        conn = get_db_connection(db_path)
        user = conn.execute(
            'SELECT * FROM admin_users WHERE id = ?',
            (user_id,)
        ).fetchone()
        conn.close()
        
        if user:
            return AdminUser(user['id'], user['username'])
        return None
    
    @staticmethod
    def get_by_username(username, db_path=None):
        """根据用户名获取用户对象"""
        conn = get_db_connection(db_path)
        user = conn.execute(
            'SELECT * FROM admin_users WHERE username = ?',
            (username,)
        ).fetchone()
        conn.close()
        
        if user:
            return AdminUser(user['id'], user['username'])
        return None
    
    @staticmethod
    def create_default_admin(db_path=None):
        """创建默认管理员账户"""
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # 检查是否已存在管理员
        existing_admin = cursor.execute(
            'SELECT COUNT(*) as count FROM admin_users WHERE username = ?',
            ('admin',)
        ).fetchone()
        
        if existing_admin['count'] == 0:
            # 默认管理员：用户名admin，密码admin123
            password_hash = PasswordManager.hash_password('admin123')
            
            cursor.execute('''
                INSERT INTO admin_users (username, password_hash)
                VALUES (?, ?)
            ''', ('admin', password_hash))
            
            conn.commit()
            print("默认管理员账户已创建: admin / admin123")
        
        conn.close()
    
    @staticmethod
    def verify_login(username, password, db_path=None):
        """验证管理员登录，返回用户对象"""
        if not username or not password:
            return None
        
        conn = get_db_connection(db_path)
        user = conn.execute(
            'SELECT * FROM admin_users WHERE username = ?',
            (username,)
        ).fetchone()
        conn.close()
        
        if user and PasswordManager.verify_password(password, user['password_hash']):
            return AdminUser(user['id'], user['username'])
        
        return None

if __name__ == '__main__':
    # 初始化数据库
    print("正在初始化数据库...")
    init_database()
    insert_default_content()
    AdminUser.create_default_admin()
    print("数据库初始化完成！")

"""
管理员API路由模块
"""
from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
import os
from config import config
from security import FileValidator, SecurityUtils
from models import TextContent, ImageContent, VideoContent, AdminUser

# 创建蓝图
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# 注意：现在使用 Flask-Login 的 @login_required 装饰器替代自定义的 require_admin_login

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """管理员登录 - 使用 Flask-Login"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        remember = data.get('remember', False)  # 记住我功能
        
        if not username or not password:
            return jsonify({
                'success': False,
                'error': '用户名和密码不能为空'
            }), 400
        
        # 在测试环境中使用测试数据库路径
        from flask import current_app
        db_path = current_app.config.get('DATABASE_PATH')
        user = AdminUser.verify_login(username, password, db_path)
        
        if user:
            # 使用 Flask-Login 登录用户
            login_user(user, remember=remember)
            return jsonify({
                'success': True,
                'message': '登录成功',
                'user': {
                    'id': user.id,
                    'username': user.username
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': '用户名或密码错误'
            }), 401
            
    except Exception as e:
        print(f"Login error: {str(e)}")  # 调试信息
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'登录过程中发生错误: {str(e)}'
        }), 500

@admin_bp.route('/logout', methods=['POST'])
def admin_logout():
    """管理员登出 - 使用 Flask-Login"""
    logout_user()
    return jsonify({
        'success': True,
        'message': '已成功登出'
    })

@admin_bp.route('/check', methods=['GET'])
def check_admin_status():
    """检查管理员登录状态 - 使用 Flask-Login"""
    if current_user.is_authenticated:
        return jsonify({
            'success': True,
            'logged_in': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username
            }
        })
    else:
        return jsonify({
            'success': False,
            'logged_in': False
        })

@admin_bp.route('/update_text', methods=['POST'])
@login_required
def update_text():
    """更新文本内容"""
    # Flask-Login 已经处理了登录检查
    
    try:
        data = request.get_json()
        element_key = data.get('element_key')
        content = data.get('content')
        
        if not element_key or content is None:
            return jsonify({
                'success': False,
                'error': 'element_key和content不能为空'
            }), 400
        
        success = TextContent.update(element_key, content)
        if success:
            return jsonify({
                'success': True,
                'message': '文本更新成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': '文本更新失败'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': '更新过程中发生错误'
        }), 500

@admin_bp.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    """上传图片"""
    # Flask-Login 已经处理了登录检查
    
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '没有选择文件'
            }), 400
        
        file = request.files['file']
        image_key = request.form.get('image_key')
        
        if not image_key:
            return jsonify({
                'success': False,
                'error': 'image_key不能为空'
            }), 400
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '没有选择文件'
            }), 400
        
        if file and FileValidator.validate_file_extension(file.filename, config.ALLOWED_EXTENSIONS):
            # 生成安全的文件名
            original_filename = SecurityUtils.sanitize_filename(file.filename)
            new_filename = SecurityUtils.generate_secure_filename(original_filename)
            
            # 确保上传目录存在
            os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
            
            # 保存文件
            file_path = os.path.join(config.UPLOAD_FOLDER, new_filename)
            file.save(file_path)
            
            # 验证文件内容
            if not FileValidator.validate_image_file(original_filename, file_path):
                os.remove(file_path)  # 删除无效文件
                return jsonify({
                    'success': False,
                    'error': '文件内容验证失败，可能不是有效的图片文件'
                }), 400
            
            # 更新数据库
            relative_path = f"/static/uploads/{new_filename}"
            success = ImageContent.update(image_key, relative_path, original_filename)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': '图片上传成功',
                    'file_path': relative_path
                })
            else:
                # 如果数据库更新失败，删除已上传的文件
                os.remove(file_path)
                return jsonify({
                    'success': False,
                    'error': '数据库更新失败'
                }), 500
        else:
            return jsonify({
                'success': False,
                'error': '不支持的文件格式'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': '上传过程中发生错误'
        }), 500

@admin_bp.route('/upload_video', methods=['POST'])
@login_required
def upload_video():
    """上传视频"""
    # Flask-Login 已经处理了登录检查
    
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '没有选择文件'
            }), 400
        
        file = request.files['file']
        video_key = request.form.get('video_key')
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        
        if not video_key:
            return jsonify({
                'success': False,
                'error': 'video_key不能为空'
            }), 400
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '没有选择文件'
            }), 400
        
        if file and FileValidator.validate_file_extension(file.filename, config.ALLOWED_VIDEO_EXTENSIONS):
            # 生成安全的文件名
            original_filename = SecurityUtils.sanitize_filename(file.filename)
            new_filename = SecurityUtils.generate_secure_filename(original_filename)
            
            # 确保上传目录存在
            os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
            
            # 保存文件
            file_path = os.path.join(config.UPLOAD_FOLDER, new_filename)
            file.save(file_path)
            
            # 验证文件内容
            if not FileValidator.validate_video_file(original_filename, file_path):
                os.remove(file_path)  # 删除无效文件
                return jsonify({
                    'success': False,
                    'error': '文件内容验证失败，可能不是有效的视频文件'
                }), 400
            
            # 获取文件大小
            file_size = os.path.getsize(file_path)
            
            # 更新数据库
            relative_path = f"/static/uploads/{new_filename}"
            success = VideoContent.update(video_key, relative_path, original_filename, title, description, None, file_size)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': '视频上传成功',
                    'file_path': relative_path
                })
            else:
                # 如果数据库更新失败，删除已上传的文件
                os.remove(file_path)
                return jsonify({
                    'success': False,
                    'error': '数据库更新失败'
                }), 500
        else:
            return jsonify({
                'success': False,
                'error': '不支持的视频文件格式'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': '上传过程中发生错误'
        }), 500

@admin_bp.route('/delete_video', methods=['POST'])
@login_required
def delete_video():
    """删除视频"""
    # Flask-Login 已经处理了登录检查
    
    try:
        data = request.get_json()
        video_key = data.get('video_key')
        
        if not video_key:
            return jsonify({
                'success': False,
                'error': 'video_key不能为空'
            }), 400
        
        # 获取视频信息
        video = VideoContent.get_by_key(video_key)
        if not video:
            return jsonify({
                'success': False,
                'error': '视频不存在'
            }), 404
        
        # 删除文件
        file_path = video['file_path']
        if file_path and file_path.startswith('/static/uploads/'):
            full_path = os.path.join(config.UPLOAD_FOLDER, os.path.basename(file_path))
            if os.path.exists(full_path):
                os.remove(full_path)
        
        # 删除数据库记录
        success = VideoContent.delete(video_key)
        if success:
            return jsonify({
                'success': True,
                'message': '视频删除成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': '删除失败'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': '删除过程中发生错误'
        }), 500

@admin_bp.route('/content', methods=['GET'])
@login_required
def get_admin_content():
    """获取管理员内容（用于后台编辑）"""
    # Flask-Login 已经处理了登录检查
    
    try:
        texts = TextContent.get_all()
        images = ImageContent.get_all()
        videos = VideoContent.get_all()
        
        return jsonify({
            'success': True,
            'data': {
                'texts': texts,
                'images': images,
                'videos': videos
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': '获取内容失败'
        }), 500

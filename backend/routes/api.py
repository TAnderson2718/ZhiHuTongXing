"""
公共API路由模块
"""
from flask import Blueprint, jsonify
from flask_wtf.csrf import CSRFProtect
from models import TextContent, ImageContent, VideoContent

# 创建蓝图
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/content', methods=['GET'])
def get_content():
    """获取所有公开内容"""
    try:
        texts = TextContent.get_all()
        images = ImageContent.get_all()
        videos = VideoContent.get_all()
        
        # 转换为前端友好的格式
        content = {
            'texts': {text['element_key']: text['content'] for text in texts},
            'images': {image['image_key']: image['file_path'] for image in images},
            'videos': {video['video_key']: {
                'file_path': video['file_path'],
                'title': video['title'],
                'description': video['description'],
                'duration': video['duration']
            } for video in videos}
        }
        
        return jsonify({
            'success': True,
            'data': content
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': '获取内容失败'
        }), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    from datetime import datetime
    return jsonify({
        'status': 'healthy',
        'success': True,
        'message': '服务运行正常',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

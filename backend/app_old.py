"""
智护童行 - Flask后端应用
"""
from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
import os
import uuid
from werkzeug.utils import secure_filename
from config import config
from security import FileValidator, SecurityUtils
from models import (
    init_database, insert_default_content, 
    TextContent, ImageContent, VideoContent, AdminUser
)

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# 启用CORS以支持前后端分离
CORS(app, supports_credentials=True, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])

# 启用CSRF保护
csrf = CSRFProtect(app)

# 配置文件上传
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

def allowed_file(filename):
    """检查图片文件扩展名是否允许"""
    return FileValidator.validate_file_extension(filename, config.ALLOWED_EXTENSIONS)

def allowed_video_file(filename):
    """检查视频文件扩展名是否允许"""
    return FileValidator.validate_file_extension(filename, config.ALLOWED_VIDEO_EXTENSIONS)

def require_admin_login():
    """检查管理员是否已登录"""
    return 'admin_logged_in' in session and session['admin_logged_in']

# ====================================================================
# 公共API - 获取内容
# ====================================================================

@app.route('/api/content', methods=['GET'])
@csrf.exempt
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
            'error': str(e)
        }), 500

# ====================================================================
# 管理员API
# ====================================================================

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """管理员登录"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'error': '用户名和密码不能为空'
            }), 400
        
        user = AdminUser.verify_login(username, password)
        if user:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return jsonify({
                'success': True,
                'message': '登录成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': '用户名或密码错误'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    """管理员登出"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return jsonify({
        'success': True,
        'message': '已成功登出'
    })

@app.route('/api/admin/check', methods=['GET'])
def check_admin_status():
    """检查管理员登录状态"""
    return jsonify({
        'success': True,
        'logged_in': require_admin_login(),
        'username': session.get('admin_username', '')
    })

@app.route('/api/admin/update_text', methods=['POST'])
def update_text():
    """更新文本内容"""
    if not require_admin_login():
        return jsonify({
            'success': False,
            'error': '需要管理员权限'
        }), 401
    
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
            'error': str(e)
        }), 500

@app.route('/api/admin/upload_image', methods=['POST'])
def upload_image():
    """上传图片"""
    if not require_admin_login():
        return jsonify({
            'success': False,
            'error': '需要管理员权限'
        }), 401
    
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
        
        if file and allowed_file(file.filename):
            # 生成安全的文件名
            original_filename = SecurityUtils.sanitize_filename(file.filename)
            new_filename = SecurityUtils.generate_secure_filename(original_filename)
            
            # 确保上传目录存在
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # 保存文件
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
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
            'error': str(e)
        }), 500

@app.route('/api/admin/upload_video', methods=['POST'])
def upload_video():
    """上传视频"""
    if not require_admin_login():
        return jsonify({
            'success': False,
            'error': '需要管理员权限'
        }), 401
    
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
        
        if file and allowed_video_file(file.filename):
            # 生成安全的文件名
            original_filename = SecurityUtils.sanitize_filename(file.filename)
            new_filename = SecurityUtils.generate_secure_filename(original_filename)
            
            # 确保上传目录存在
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # 保存文件
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
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
            'error': str(e)
        }), 500

@app.route('/api/admin/delete_video', methods=['POST'])
def delete_video():
    """删除视频"""
    if not require_admin_login():
        return jsonify({
            'success': False,
            'error': '需要管理员权限'
        }), 401
    
    try:
        data = request.get_json()
        video_key = data.get('video_key')
        
        if not video_key:
            return jsonify({
                'success': False,
                'error': 'video_key不能为空'
            }), 400
        
        # 获取视频信息用于删除文件
        video = VideoContent.get_by_key(video_key)
        
        # 从数据库删除
        success = VideoContent.delete(video_key)
        
        if success and video:
            # 删除物理文件
            try:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(video['file_path']))
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass  # 即使文件删除失败，也返回成功
            
            return jsonify({
                'success': True,
                'message': '视频删除成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': '视频删除失败'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/content', methods=['GET'])
def get_admin_content():
    """获取管理员内容（用于后台编辑）"""
    if not require_admin_login():
        return jsonify({
            'success': False,
            'error': '需要管理员权限'
        }), 401
    
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
            'error': str(e)
        }), 500

# ====================================================================
# 静态文件服务
# ====================================================================

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """提供上传的文件"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ====================================================================
# 管理后台页面
# ====================================================================

@app.route('/admin')
def admin_dashboard():
    """管理后台首页"""
    return '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>智护童行 - 管理后台</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
        <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    </head>
    <body class="bg-gray-100">
        <div id="admin-app">
            <!-- 登录表单 -->
            <div v-if="!isLoggedIn" class="min-h-screen flex items-center justify-center">
                <div class="bg-white p-8 rounded-lg shadow-md w-96">
                    <h2 class="text-2xl font-bold mb-6 text-center">管理员登录</h2>
                    <form @submit.prevent="login">
                        <div class="mb-4">
                            <label class="block text-gray-700 text-sm font-bold mb-2">用户名</label>
                            <input v-model="loginForm.username" type="text" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500" required>
                        </div>
                        <div class="mb-6">
                            <label class="block text-gray-700 text-sm font-bold mb-2">密码</label>
                            <input v-model="loginForm.password" type="password" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500" required>
                        </div>
                        <button type="submit" class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600">登录</button>
                    </form>
                    <div v-if="loginError" class="mt-4 text-red-500 text-sm">{{ loginError }}</div>
                </div>
            </div>
            
            <!-- 管理界面 -->
            <div v-if="isLoggedIn" class="min-h-screen">
                <!-- 顶部导航 -->
                <nav class="bg-white shadow-sm border-b">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div class="flex justify-between h-16">
                            <div class="flex items-center">
                                <h1 class="text-xl font-semibold">智护童行 - 内容管理</h1>
                            </div>
                            <div class="flex items-center">
                                <span class="mr-4">欢迎，{{ username }}</span>
                                <button @click="logout" class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">登出</button>
                            </div>
                        </div>
                    </div>
                </nav>
                
                <!-- 主要内容 -->
                <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                    <!-- 标签页 -->
                    <div class="mb-6">
                        <div class="border-b border-gray-200">
                            <nav class="-mb-px flex space-x-8">
                                <button @click="activeTab = 'texts'" :class="{'border-blue-500 text-blue-600': activeTab === 'texts', 'border-transparent text-gray-500': activeTab !== 'texts'}" class="whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm">文本内容</button>
                                <button @click="activeTab = 'images'" :class="{'border-blue-500 text-blue-600': activeTab === 'images', 'border-transparent text-gray-500': activeTab !== 'images'}" class="whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm">图片内容</button>
                                <button @click="activeTab = 'videos'" :class="{'border-blue-500 text-blue-600': activeTab === 'videos', 'border-transparent text-gray-500': activeTab !== 'videos'}" class="whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm">视频内容</button>
                            </nav>
                        </div>
                    </div>
                    
                    <!-- 文本内容管理 -->
                    <div v-if="activeTab === 'texts'" class="bg-white shadow rounded-lg">
                        <div class="px-6 py-4 border-b border-gray-200">
                            <h3 class="text-lg font-medium">文本内容管理</h3>
                        </div>
                        <div class="p-6">
                            <div v-for="text in texts" :key="text.id" class="mb-6 p-4 border rounded-lg">
                                <label class="block text-sm font-medium text-gray-700 mb-2">{{ text.element_key }}</label>
                                <textarea v-model="text.content" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" rows="3"></textarea>
                                <button @click="updateText(text.element_key, text.content)" class="mt-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">保存</button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 图片内容管理 -->
                    <div v-if="activeTab === 'images'" class="bg-white shadow rounded-lg">
                        <div class="px-6 py-4 border-b border-gray-200">
                            <h3 class="text-lg font-medium">图片内容管理</h3>
                        </div>
                        <div class="p-6">
                            <div v-for="image in images" :key="image.id" class="mb-6 p-4 border rounded-lg">
                                <label class="block text-sm font-medium text-gray-700 mb-2">{{ image.image_key }}</label>
                                <div class="flex items-center space-x-4">
                                    <img v-if="image.file_path" :src="image.file_path" class="w-20 h-20 object-cover rounded">
                                    <div>
                                        <input type="file" @change="handleFileSelect($event, image.image_key)" accept="image/*" class="mb-2">
                                        <button @click="uploadImage(image.image_key)" :disabled="!selectedFiles[image.image_key]" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:bg-gray-400">上传图片</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 视频内容管理 -->
                    <div v-if="activeTab === 'videos'" class="bg-white shadow rounded-lg">
                        <div class="px-6 py-4 border-b border-gray-200">
                            <h3 class="text-lg font-medium">视频内容管理</h3>
                        </div>
                        <div class="p-6">
                            <!-- 新增视频 -->
                            <div class="mb-8 p-4 border-2 border-dashed border-gray-300 rounded-lg">
                                <h4 class="text-md font-medium mb-4">新增视频</h4>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">Video Key</label>
                                        <input v-model="newVideo.key" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="例如: newborn_care_demo">
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">标题</label>
                                        <input v-model="newVideo.title" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="视频标题">
                                    </div>
                                </div>
                                <div class="mb-4">
                                    <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
                                    <textarea v-model="newVideo.description" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" rows="2" placeholder="视频描述"></textarea>
                                </div>
                                <div class="flex items-center space-x-4">
                                    <input type="file" @change="handleVideoFileSelect" accept="video/*" class="flex-1">
                                    <button @click="uploadNewVideo" :disabled="!newVideo.file || !newVideo.key" class="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400">上传视频</button>
                                </div>
                            </div>
                            
                            <!-- 已有视频列表 -->
                            <div v-for="video in videos" :key="video.id" class="mb-6 p-4 border rounded-lg">
                                <div class="flex justify-between items-start mb-3">
                                    <div class="flex-1">
                                        <label class="block text-sm font-medium text-gray-700 mb-1">{{ video.video_key }}</label>
                                        <h4 class="text-lg font-semibold">{{ video.title || '未命名视频' }}</h4>
                                        <p class="text-gray-600 text-sm">{{ video.description || '无描述' }}</p>
                                    </div>
                                    <button @click="deleteVideo(video.video_key)" class="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600">删除</button>
                                </div>
                                
                                <div class="flex items-center space-x-4">
                                    <div v-if="video.file_path" class="flex-1">
                                        <video :src="video.file_path" class="w-full max-w-md h-40 object-cover rounded" controls></video>
                                        <p class="text-xs text-gray-500 mt-1">
                                            文件大小: {{ formatFileSize(video.file_size) }} | 
                                            创建时间: {{ formatDate(video.created_at) }}
                                        </p>
                                    </div>
                                    <div>
                                        <input type="file" @change="handleVideoReplaceSelect($event, video.video_key)" accept="video/*" class="mb-2">
                                        <button @click="replaceVideo(video.video_key)" :disabled="!selectedVideoFiles[video.video_key]" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:bg-gray-400 block">更换视频</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            const { createApp } = Vue;
            
            createApp({
                data() {
                    return {
                        isLoggedIn: false,
                        username: '',
                        activeTab: 'texts',
                        loginForm: {
                            username: '',
                            password: ''
                        },
                        loginError: '',
                        texts: [],
                        images: [],
                        videos: [],
                        selectedFiles: {},
                        selectedVideoFiles: {},
                        newVideo: {
                            key: '',
                            title: '',
                            description: '',
                            file: null
                        }
                    }
                },
                async mounted() {
                    await this.checkLoginStatus();
                    if (this.isLoggedIn) {
                        await this.loadContent();
                    }
                },
                methods: {
                    async checkLoginStatus() {
                        try {
                            const response = await axios.get('/api/admin/check');
                            this.isLoggedIn = response.data.logged_in;
                            this.username = response.data.username;
                        } catch (error) {
                            console.error('检查登录状态失败:', error);
                        }
                    },
                    async login() {
                        try {
                            const response = await axios.post('/api/admin/login', this.loginForm);
                            if (response.data.success) {
                                this.isLoggedIn = true;
                                this.username = this.loginForm.username;
                                this.loginError = '';
                                await this.loadContent();
                            }
                        } catch (error) {
                            this.loginError = error.response?.data?.error || '登录失败';
                        }
                    },
                    async logout() {
                        try {
                            await axios.post('/api/admin/logout');
                            this.isLoggedIn = false;
                            this.username = '';
                        } catch (error) {
                            console.error('登出失败:', error);
                        }
                    },
                    async loadContent() {
                        try {
                            const response = await axios.get('/api/admin/content');
                            if (response.data.success) {
                                this.texts = response.data.data.texts;
                                this.images = response.data.data.images;
                                this.videos = response.data.data.videos;
                            }
                        } catch (error) {
                            console.error('加载内容失败:', error);
                        }
                    },
                    async updateText(elementKey, content) {
                        try {
                            const response = await axios.post('/api/admin/update_text', {
                                element_key: elementKey,
                                content: content
                            });
                            if (response.data.success) {
                                alert('文本更新成功！');
                            }
                        } catch (error) {
                            alert('更新失败: ' + (error.response?.data?.error || '未知错误'));
                        }
                    },
                    handleFileSelect(event, imageKey) {
                        const file = event.target.files[0];
                        if (file) {
                            this.selectedFiles[imageKey] = file;
                        }
                    },
                    async uploadImage(imageKey) {
                        const file = this.selectedFiles[imageKey];
                        if (!file) return;
                        
                        const formData = new FormData();
                        formData.append('file', file);
                        formData.append('image_key', imageKey);
                        
                        try {
                            const response = await axios.post('/api/admin/upload_image', formData, {
                                headers: {
                                    'Content-Type': 'multipart/form-data'
                                }
                            });
                            if (response.data.success) {
                                alert('图片上传成功！');
                                await this.loadContent(); // 重新加载内容
                                delete this.selectedFiles[imageKey];
                            }
                        } catch (error) {
                            alert('上传失败: ' + (error.response?.data?.error || '未知错误'));
                        }
                    },
                    
                    // 视频管理相关方法
                    handleVideoFileSelect(event) {
                        const file = event.target.files[0];
                        if (file) {
                            this.newVideo.file = file;
                        }
                    },
                    
                    handleVideoReplaceSelect(event, videoKey) {
                        const file = event.target.files[0];
                        if (file) {
                            this.selectedVideoFiles[videoKey] = file;
                        }
                    },
                    
                    async uploadNewVideo() {
                        if (!this.newVideo.file || !this.newVideo.key) {
                            alert('请填写完整信息并选择视频文件！');
                            return;
                        }
                        
                        const formData = new FormData();
                        formData.append('file', this.newVideo.file);
                        formData.append('video_key', this.newVideo.key);
                        formData.append('title', this.newVideo.title);
                        formData.append('description', this.newVideo.description);
                        
                        try {
                            const response = await axios.post('/api/admin/upload_video', formData, {
                                headers: {
                                    'Content-Type': 'multipart/form-data'
                                }
                            });
                            if (response.data.success) {
                                alert('视频上传成功！');
                                await this.loadContent();
                                // 清空表单
                                this.newVideo = {
                                    key: '',
                                    title: '',
                                    description: '',
                                    file: null
                                };
                            }
                        } catch (error) {
                            alert('上传失败: ' + (error.response?.data?.error || '未知错误'));
                        }
                    },
                    
                    async replaceVideo(videoKey) {
                        const file = this.selectedVideoFiles[videoKey];
                        if (!file) return;
                        
                        const formData = new FormData();
                        formData.append('file', file);
                        formData.append('video_key', videoKey);
                        
                        try {
                            const response = await axios.post('/api/admin/upload_video', formData, {
                                headers: {
                                    'Content-Type': 'multipart/form-data'
                                }
                            });
                            if (response.data.success) {
                                alert('视频更换成功！');
                                await this.loadContent();
                                delete this.selectedVideoFiles[videoKey];
                            }
                        } catch (error) {
                            alert('更换失败: ' + (error.response?.data?.error || '未知错误'));
                        }
                    },
                    
                    async deleteVideo(videoKey) {
                        if (!confirm('确定要删除这个视频吗？此操作不可恢复！')) {
                            return;
                        }
                        
                        try {
                            const response = await axios.post('/api/admin/delete_video', {
                                video_key: videoKey
                            });
                            if (response.data.success) {
                                alert('视频删除成功！');
                                await this.loadContent();
                            }
                        } catch (error) {
                            alert('删除失败: ' + (error.response?.data?.error || '未知错误'));
                        }
                    },
                    
                    // 工具方法
                    formatFileSize(bytes) {
                        if (!bytes) return '未知';
                        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                        const i = Math.floor(Math.log(bytes) / Math.log(1024));
                        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
                    },
                    
                    formatDate(dateString) {
                        if (!dateString) return '未知';
                        return new Date(dateString).toLocaleString('zh-CN');
                    }
                }
            }).mount('#admin-app');
        </script>
    </body>
    </html>
    '''

# ====================================================================
# 错误处理
# ====================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': '接口不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': '服务器内部错误'
    }), 500

# ====================================================================
# 应用初始化
# ====================================================================

if __name__ == '__main__':
    # 初始化数据库
    init_database()
    insert_default_content()
    AdminUser.create_default_admin()
    
    print("智护童行后端服务启动中...")
    print(f"管理后台地址: http://{config.HOST}:{config.PORT}/admin")
    print("默认管理员账户: admin / admin123")
    print("注意：生产环境请修改默认密码并设置环境变量！")
    
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)

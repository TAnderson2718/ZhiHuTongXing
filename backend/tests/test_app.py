import pytest
import json
import os
import tempfile
from app import create_app
from models import init_database

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE_PATH': db_path,
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False,  # Disable CSRF for testing
    })
    
    with app.app_context():
        init_database(db_path)
        # 创建默认管理员账户用于测试
        from models import AdminUser
        AdminUser.create_default_admin(db_path)
    
    yield app
    
    # Clean up
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

class TestHealthEndpoint:
    """Test the health check endpoint."""
    
    def test_health_endpoint(self, client):
        """Test that health endpoint returns success."""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data

class TestContentEndpoint:
    """Test the content API endpoint."""
    
    def test_content_endpoint(self, client):
        """Test that content endpoint returns data."""
        response = client.get('/api/content')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
        assert 'texts' in data['data']
        assert 'images' in data['data']

class TestAdminEndpoints:
    """Test admin-related endpoints."""
    
    def test_admin_check_unauthorized(self, client):
        """Test admin check without authentication."""
        response = client.get('/api/admin/check')
        assert response.status_code == 401
    
    def test_admin_login_invalid_credentials(self, client):
        """Test admin login with invalid credentials."""
        response = client.post('/api/admin/login', json={
            'username': 'invalid',
            'password': 'invalid'
        })
        assert response.status_code == 401
        
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_admin_login_valid_credentials(self, client):
        """Test admin login with valid credentials."""
        response = client.post('/api/admin/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['message'] == '登录成功'

class TestStaticFiles:
    """Test static file serving."""
    
    def test_admin_page(self, client):
        """Test that admin page is accessible."""
        response = client.get('/admin')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
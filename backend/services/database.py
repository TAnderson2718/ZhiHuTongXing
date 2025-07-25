"""
数据库连接池服务
"""
import sqlite3
import threading
import queue
import time
from contextlib import contextmanager
from config import config

class DatabasePool:
    """SQLite连接池"""
    
    def __init__(self, database_path: str, max_connections: int = 10, timeout: int = 30):
        self.database_path = database_path
        self.max_connections = max_connections
        self.timeout = timeout
        self._pool = queue.Queue(maxsize=max_connections)
        self._lock = threading.Lock()
        self._created_connections = 0
        
        # 预创建一些连接
        self._initialize_pool()
    
    def _initialize_pool(self):
        """初始化连接池"""
        # 创建初始连接（池大小的一半）
        initial_size = max(1, self.max_connections // 2)
        for _ in range(initial_size):
            conn = self._create_connection()
            if conn:
                self._pool.put(conn)
    
    def _create_connection(self):
        """创建新的数据库连接"""
        try:
            conn = sqlite3.connect(
                self.database_path,
                check_same_thread=False,  # 允许多线程使用
                timeout=self.timeout
            )
            conn.row_factory = sqlite3.Row  # 使查询结果可以像字典一样访问
            
            # 设置一些性能优化选项
            conn.execute('PRAGMA journal_mode=WAL')  # 启用WAL模式
            conn.execute('PRAGMA synchronous=NORMAL')  # 平衡性能和安全性
            conn.execute('PRAGMA cache_size=10000')  # 增加缓存大小
            conn.execute('PRAGMA temp_store=MEMORY')  # 临时表存储在内存中
            
            with self._lock:
                self._created_connections += 1
            
            return conn
        except sqlite3.Error as e:
            print(f"创建数据库连接失败: {e}")
            return None
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = None
        try:
            # 尝试从池中获取连接
            try:
                conn = self._pool.get(timeout=5)
            except queue.Empty:
                # 池中没有可用连接，创建新连接
                if self._created_connections < self.max_connections:
                    conn = self._create_connection()
                    if not conn:
                        raise Exception("无法创建新的数据库连接")
                else:
                    # 等待连接可用
                    conn = self._pool.get(timeout=self.timeout)
            
            # 检查连接是否仍然有效
            if not self._is_connection_valid(conn):
                conn.close()
                conn = self._create_connection()
                if not conn:
                    raise Exception("无法创建有效的数据库连接")
            
            yield conn
            
        except Exception as e:
            if conn:
                try:
                    conn.rollback()  # 回滚任何未提交的事务
                except:
                    pass
            raise e
        finally:
            # 将连接返回池中
            if conn:
                try:
                    # 确保没有未提交的事务
                    conn.rollback()
                    self._pool.put(conn, timeout=1)
                except (queue.Full, sqlite3.Error):
                    # 池已满或连接有问题，关闭连接
                    try:
                        conn.close()
                    except:
                        pass
                    with self._lock:
                        self._created_connections -= 1
    
    def _is_connection_valid(self, conn):
        """检查连接是否有效"""
        try:
            conn.execute('SELECT 1').fetchone()
            return True
        except sqlite3.Error:
            return False
    
    def close_all(self):
        """关闭所有连接"""
        while not self._pool.empty():
            try:
                conn = self._pool.get_nowait()
                conn.close()
            except (queue.Empty, sqlite3.Error):
                break
        
        with self._lock:
            self._created_connections = 0
    
    def get_stats(self):
        """获取连接池统计信息"""
        return {
            'pool_size': self._pool.qsize(),
            'max_connections': self.max_connections,
            'created_connections': self._created_connections,
            'available_connections': self._pool.qsize()
        }

# 全局连接池实例
_db_pool = None

def get_db_pool():
    """获取数据库连接池实例"""
    global _db_pool
    if _db_pool is None:
        _db_pool = DatabasePool(config.DATABASE_PATH)
    return _db_pool

def init_database_pool():
    """初始化数据库连接池"""
    global _db_pool
    if _db_pool is None:
        _db_pool = DatabasePool(config.DATABASE_PATH)
    return _db_pool

def close_database_pool():
    """关闭数据库连接池"""
    global _db_pool
    if _db_pool:
        _db_pool.close_all()
        _db_pool = None

@contextmanager
def get_db_connection():
    """获取数据库连接的便捷函数"""
    pool = get_db_pool()
    with pool.get_connection() as conn:
        yield conn

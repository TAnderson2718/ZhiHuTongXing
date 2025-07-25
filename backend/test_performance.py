#!/usr/bin/env python3
"""
架构重构性能测试脚本
"""
import time
import concurrent.futures
import requests
import statistics
from services.database import get_db_pool

def test_api_performance():
    """测试API响应性能"""
    base_url = "http://127.0.0.1:5001"
    endpoints = [
        "/api/health",
        "/api/content",
        "/api/admin/check"
    ]
    
    print("🚀 API性能测试开始...")
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        response_times = []
        
        # 进行10次请求测试
        for i in range(10):
            start_time = time.time()
            try:
                response = requests.get(url, timeout=5)
                end_time = time.time()
                
                if response.status_code == 200:
                    response_times.append((end_time - start_time) * 1000)  # 转换为毫秒
                else:
                    print(f"❌ {endpoint} 返回状态码: {response.status_code}")
            except Exception as e:
                print(f"❌ {endpoint} 请求失败: {e}")
        
        if response_times:
            avg_time = statistics.mean(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
            
            print(f"✅ {endpoint}")
            print(f"   平均响应时间: {avg_time:.2f}ms")
            print(f"   最快响应时间: {min_time:.2f}ms")
            print(f"   最慢响应时间: {max_time:.2f}ms")
        print()

def test_database_pool():
    """测试数据库连接池性能"""
    print("🗄️ 数据库连接池测试开始...")
    
    pool = get_db_pool()
    
    # 显示连接池初始状态
    stats = pool.get_stats()
    print(f"初始连接池状态:")
    print(f"  最大连接数: {stats['max_connections']}")
    print(f"  当前连接数: {stats['created_connections']}")
    print(f"  可用连接数: {stats['available_connections']}")
    print()
    
    def execute_query(query_id):
        """执行单个数据库查询"""
        start_time = time.time()
        try:
            with pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) as count FROM text_content")
                result = cursor.fetchone()
                end_time = time.time()
                return {
                    'query_id': query_id,
                    'success': True,
                    'time': (end_time - start_time) * 1000,
                    'result': dict(result) if result else None
                }
        except Exception as e:
            end_time = time.time()
            return {
                'query_id': query_id,
                'success': False,
                'time': (end_time - start_time) * 1000,
                'error': str(e)
            }
    
    # 并发测试
    print("执行并发数据库查询测试...")
    concurrent_queries = 20
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(execute_query, i) for i in range(concurrent_queries)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    # 分析结果
    successful_queries = [r for r in results if r['success']]
    failed_queries = [r for r in results if not r['success']]
    
    if successful_queries:
        response_times = [r['time'] for r in successful_queries]
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        print(f"✅ 并发查询结果:")
        print(f"   成功查询: {len(successful_queries)}/{concurrent_queries}")
        print(f"   失败查询: {len(failed_queries)}")
        print(f"   平均查询时间: {avg_time:.2f}ms")
        print(f"   最快查询时间: {min_time:.2f}ms")
        print(f"   最慢查询时间: {max_time:.2f}ms")
    
    if failed_queries:
        print(f"❌ 失败的查询:")
        for failed in failed_queries[:3]:  # 只显示前3个错误
            print(f"   查询 {failed['query_id']}: {failed['error']}")
    
    # 显示连接池最终状态
    final_stats = pool.get_stats()
    print(f"\n连接池最终状态:")
    print(f"  创建的连接数: {final_stats['created_connections']}")
    print(f"  可用连接数: {final_stats['available_connections']}")
    print()

def test_concurrent_api_requests():
    """测试并发API请求"""
    print("🔄 并发API请求测试开始...")
    
    base_url = "http://127.0.0.1:5001"
    endpoint = "/api/content"
    concurrent_requests = 15
    
    def make_request(request_id):
        """发起单个API请求"""
        start_time = time.time()
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            end_time = time.time()
            return {
                'request_id': request_id,
                'success': response.status_code == 200,
                'time': (end_time - start_time) * 1000,
                'status_code': response.status_code
            }
        except Exception as e:
            end_time = time.time()
            return {
                'request_id': request_id,
                'success': False,
                'time': (end_time - start_time) * 1000,
                'error': str(e)
            }
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request, i) for i in range(concurrent_requests)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    successful_requests = [r for r in results if r['success']]
    failed_requests = [r for r in results if not r['success']]
    
    if successful_requests:
        response_times = [r['time'] for r in successful_requests]
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        print(f"✅ 并发API请求结果:")
        print(f"   成功请求: {len(successful_requests)}/{concurrent_requests}")
        print(f"   失败请求: {len(failed_requests)}")
        print(f"   平均响应时间: {avg_time:.2f}ms")
        print(f"   最快响应时间: {min_time:.2f}ms")
        print(f"   最慢响应时间: {max_time:.2f}ms")
    
    if failed_requests:
        print(f"❌ 失败的请求:")
        for failed in failed_requests[:3]:
            print(f"   请求 {failed['request_id']}: {failed.get('error', '状态码错误')}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 智护童行架构重构性能测试")
    print("=" * 60)
    print()
    
    try:
        # 1. API性能测试
        test_api_performance()
        
        # 2. 数据库连接池测试
        test_database_pool()
        
        # 3. 并发API请求测试
        test_concurrent_api_requests()
        
        print("=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        print("请确保后端服务正在运行 (python3 app.py)")

# 代码生成时间: 2025-09-01 23:22:13
import asyncio
import httpx
from quart import Quart, jsonify

# 定义一个Quart应用
app = Quart(__name__)

# 性能测试函数
async def perform_test(url, requests_count):
    async with httpx.AsyncClient() as client:
        try:
            tasks = [client.get(url) for _ in range(requests_count)]
            responses = await asyncio.gather(*tasks)
            # 计算平均响应时间
            total_time = sum(response.elapsed.total_seconds() for response in responses)
            avg_time = total_time / requests_count
            return {
                'total_requests': requests_count,
                'total_time': total_time,
                'average_time': avg_time
            }
        except Exception as e:
            # 错误处理
            return {'error': str(e)}

# API端点，执行性能测试
@app.route('/perform_test', methods=['POST'])
async def perform_test_api():
    data = await request.get_json()
    url = data.get('url')
    requests_count = data.get('requests_count')
    if url is None or requests_count is None:
        return jsonify({'error': 'Missing URL or requests count'})
    response = await perform_test(url, requests_count)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
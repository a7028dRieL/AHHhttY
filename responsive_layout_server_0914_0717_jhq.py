# 代码生成时间: 2025-09-14 07:17:24
# responsive_layout_server.py

"""
使用Quart框架创建一个简单的响应式布局服务器。
这个服务器将提供一个路由，该路由可以根据请求头中的'Accept'字段返回不同格式的响应。
"""

from quart import Quart, request, jsonify

app = Quart(__name__)

@app.route('/response')
async def responsive_response():
    # 检查请求头中的'Accept'字段，确定响应的内容类型
    accept_header = request.headers.get('Accept', 'application/json')
    
    # 根据'Accept'字段的内容返回相应的响应
    if 'application/json' in accept_header:
        return jsonify({'message': 'This is a JSON response'}), 200, {'Content-Type': 'application/json'}
    elif 'text/html' in accept_header:
        return "<html><body><h1>This is an HTML response</h1></body></html>", 200, {'Content-Type': 'text/html'}
    else:
        # 如果'Accept'字段不符合预期，返回错误信息
        return jsonify({'error': 'Unsupported media type'}), 415, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    # 运行服务，默认端口5000
    app.run(debug=True)
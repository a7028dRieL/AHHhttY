# 代码生成时间: 2025-08-18 15:15:21
from quart import Quart, request, jsonify

# 创建一个Quart应用实例
def create_app():
    app = Quart(__name__)

    # 模拟用户数据库
    users = {"admin": "password123"}

    @app.route('/login', methods=['POST'])
    async def login():
        # 获取请求中的用户名和密码
        username = request.json.get('username')
        password = request.json.get('password')

        # 错误处理
        if not username or not password:
            return jsonify(error="Both username and password are required"), 400

        # 用户验证
        if users.get(username) == password:
            return jsonify(message="Login successful"), 200
        else:
            return jsonify(error="Invalid username or password"), 401

    return app

# 主函数
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
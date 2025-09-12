# 代码生成时间: 2025-09-12 14:01:02
from quart import Quart, request, jsonify

# 初始化Quart应用
app = Quart(__name__)

# 用户信息字典，用于模拟数据库
users = {"user1": {"password": "password1"}, "user2": {"password": "password2"}}

# 身份认证装饰器
def authenticate(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # 从请求头中获取用户名和密码
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({'message': 'Missing or invalid credentials'}), 401

        # 验证用户名和密码
        if auth.username in users and users[auth.username]['password'] == auth.password:
            return await func(*args, **kwargs)
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

        return await func(*args, **kwargs)
    return wrapper

# 受保护的路由
@app.route("/protected")
@authenticate
async def protected_route():
    # 仅当用户身份认证通过时执行
    return jsonify({'message': 'Access granted to protected route'})

# 未受保护的路由，用于获取用户输入
@app.route("/login", methods=['POST'])
async def login():
    # 验证请求数据
    data = await request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing credentials'}), 400

    # 验证用户名和密码
    username = data['username']
    password = data['password']
    if username in users and users[username]['password'] == password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)

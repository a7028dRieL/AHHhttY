# 代码生成时间: 2025-09-16 16:14:02
import quart as q
from quart import jsonify, request
from quart_cors import cors
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 数据库配置
DATABASE = 'user_auth.db'

# 创建 Quart 应用
app = q.Quart(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
app.config['SECRET_KEY'] = 'your_secret_key_here'
cors(app)

# 初始化数据库
db = SQLAlchemy(app)

# 用户模型
class User(db.Model):
    '''用户模型类'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        '''设置密码'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''检查密码'''
        return check_password_hash(self.password_hash, password)

# 添加用户路由
@app.route('/add_user', methods=['POST'])
async def add_user():
    '''添加用户接口'''
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409
    user = User(username=username)
    user.set_password(password)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 用户登录路由
@app.route('/login', methods=['POST'])
async def login():
    '''用户登录接口'''
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    return jsonify({'message': 'Login successful'}), 200

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
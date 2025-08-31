# 代码生成时间: 2025-08-31 23:40:42
from quart import Quart, jsonify
from marshmallow import Schema, fields, ValidationError, EXCLUDE
from quart_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 数据模型基类
Base = declarative_base()

# 数据库配置
DATABASE_URI = 'sqlite:///example.db'
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 数据模型
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(120), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

# 数据库初始化
Base.metadata.create_all(bind=engine)

# 应用配置
app = Quart(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 用户数据模型验证
class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)

    class Meta:
        unknown = EXCLUDE

# 错误处理
@app.errorhandler(ValidationError)
async def handle_validation_error(error):
    return jsonify(error.messages), 400

# API 路由
@app.route('/users/', methods=['POST'])
async def create_user():
    try:
        schema = UserSchema()
        data = await request.get_json()
        result = schema.load(data)
        user = User(**result)
        db.session.add(user)
        await db.session.commit()
        return jsonify(schema.dump(user)), 201
    except ValidationError as err:
        raise err

@app.route('/users/<int:user_id>/', methods=['GET'])
async def get_user(user_id):
    user = await get_user_by_id(user_id)
    if user:
        schema = UserSchema()
        return jsonify(schema.dump(user)), 200
    return jsonify({'message': 'User not found'}), 404

# 辅助函数
async def get_user_by_id(user_id):
    async with SessionLocal() as session:
        user = session.query(User).filter(User.id == user_id).first()
        return user

# 运行应用
if __name__ == '__main__':
    app.run()

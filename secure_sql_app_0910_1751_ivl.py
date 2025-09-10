# 代码生成时间: 2025-09-10 17:51:54
# Secure SQL App using Quart and SQLAlchemy

from quart import Quart, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select

# Define the Quart app
app = Quart(__name__)

# Database configuration
DATABASE_URI = 'sqlite:///secure_sql.db'  # Replace with your actual database URI

# Initialize the database engine and session
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a simple User model for demonstration purposes
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

# Initialize the database tables
Base.metadata.create_all(bind=engine)

# Route to demonstrate a secure SQL query
@app.route('/get_user', methods=['GET'])
async def get_user():
    # Get the username from the query parameters
    username = request.args.get('username')

    if not username:
        return jsonify({'error': 'Username parameter is missing'}), 400

    # Use SQLAlchemy Core to prevent SQL injection by using a bind parameter
    try:
        session = SessionLocal()
        user = session.execute(
            text("SELECT * FROM users WHERE username = :username"), {'username': username}
        ).scalars().first()

        if user:
            return jsonify({'user': {'id': user.id, 'username': user.username, 'email': user.email}})
        else:
            return jsonify({'message': 'User not found'}), 404
    except SQLAlchemyError as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        session.close()

# Route to demonstrate a secure SQL query for inserting data
@app.route('/add_user', methods=['POST'])
async def add_user():
    # Get the username and email from the JSON data
    user_data = await request.get_json()
    username = user_data.get('username')
    email = user_data.get('email')

    if not username or not email:
        return jsonify({'error': 'Username and email are required'}), 400

    try:
        session = SessionLocal()
        new_user = User(username=username, email=email)
        session.add(new_user)
        session.commit()
        return jsonify({'message': 'User added successfully', 'user': {'id': new_user.id, 'username': new_user.username, 'email': new_user.email}}), 201
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run()

# 代码生成时间: 2025-09-12 01:53:32
import quart
from quart import jsonify
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

# 设置密钥生成函数
def generate_key(password: str, salt: bytes) -> bytes:
    """
    根据给定的密码和盐生成加密密钥。
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# 设置加密和解密函数
def encrypt_message(key: bytes, message: str) -> bytes:
    """
    使用给定的密钥对消息进行加密。
    """
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(key: bytes, token: bytes) -> str:
    """
    使用给定的密钥对token进行解密。
    """
    f = Fernet(key)
    return f.decrypt(token).decode()

# Quart蓝图对象
app = quart.Quart(__name__)

# 密码加密API
@app.route('/encrypt', methods=['POST'])
async def encrypt_api():
    """
    接收密码和盐，返回加密后的密码。
    """
    data = await quart.request.get_json()
    if not data or 'password' not in data or 'salt' not in data:
        return jsonify({'error': 'Missing password or salt'}), 400
    
    password = data['password']
    salt = urlsafe_b64decode(data['salt'])
    key = generate_key(password, salt)
    encrypted_password = encrypt_message(key, password)
    return jsonify({'encrypted_password': urlsafe_b64encode(encrypted_password).decode()})

# 密码解密API
@app.route('/decrypt', methods=['POST'])
async def decrypt_api():
    """
    接收密码和加密后的token，返回解密后的密码。
    """
    data = await quart.request.get_json()
    if not data or 'password' not in data or 'encrypted_token' not in data:
        return jsonify({'error': 'Missing password or encrypted token'}), 400
    
    password = data['password']
    encrypted_token = urlsafe_b64decode(data['encrypted_token'])
    salt = os.urandom(16)  # 生成新的盐
    key = generate_key(password, salt)
    try:
        decrypted_password = decrypt_message(key, encrypted_token)
        return jsonify({'decrypted_password': decrypted_password})
    except quart.exceptions. quart.exceptions. quart.exceptions.QuartException:
        return jsonify({'error': 'Invalid encrypted token or password'}), 400

# 运行Quart应用
if __name__ == '__main__':
    app.run()

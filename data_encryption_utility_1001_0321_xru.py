# 代码生成时间: 2025-10-01 03:21:26
import quart
from quart import jsonify
from cryptography.fernet import Fernet

# 生成密钥函数
def generate_key():
    """Generate a key for encryption.

    Returns:
        bytes: A generated key for encryption.
    """
    return Fernet.generate_key()

# 加密函数
def encrypt_data(key, data):
    """Encrypt data using the given key.

    Args:
        key (bytes): The encryption key.
        data (str): The data to be encrypted.

    Returns:
        str: Encrypted data.
    """
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

# 解密函数
def decrypt_data(key, encrypted_data):
    """Decrypt data using the given key.

    Args:
        key (bytes): The encryption key.
        encrypted_data (str): The encrypted data to be decrypted.

    Returns:
        str: Decrypted data.
    """
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data.encode()).decode()

# Quart application
app = quart.Quart(__name__)

# 获取密钥端点
@app.route('/get_key', methods=['GET'])
async def get_key():
    """Endpoint to get a new encryption key.

    Returns:
        A JSON response containing the generated key.
    """
    try:
        key = generate_key()
        return jsonify({'key': key.decode()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 加密端点
@app.route('/encrypt', methods=['POST'])
async def encrypt():
    """Endpoint to encrypt data.

    Returns:
        A JSON response containing the encrypted data.
    """
    data = await quart.request.get_json()
    if 'key' not in data or 'data' not in data:
        return jsonify({'error': 'Missing key or data'}), 400
    try:
        encrypted_data = encrypt_data(data['key'].encode(), data['data'])
        return jsonify({'encrypted_data': encrypted_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 解密端点
@app.route('/decrypt', methods=['POST'])
async def decrypt():
    """Endpoint to decrypt data.

    Returns:
        A JSON response containing the decrypted data.
    """
    encrypted_data = await quart.request.get_json()
    if 'key' not in encrypted_data or 'data' not in encrypted_data:
        return jsonify({'error': 'Missing key or data'}), 400
    try:
        decrypted_data = decrypt_data(encrypted_data['key'].encode(), encrypted_data['data'])
        return jsonify({'decrypted_data': decrypted_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
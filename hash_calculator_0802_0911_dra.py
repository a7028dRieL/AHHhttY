# 代码生成时间: 2025-08-02 09:11:01
import quart
from quart import request, jsonify
from hashlib import md5, sha1, sha256, sha512

class HashCalculator:
    # 定义支持的哈希算法列表
    algorithms = [
        'md5',
        'sha1',
        'sha256',
        'sha512'
    ]

    def __init__(self):
        pass

    def calculate_hash(self, text: str, algorithm: str) -> str:
        # 根据提供的算法计算哈希值
        if algorithm not in self.algorithms:
            raise ValueError(f'Unsupported algorithm: {algorithm}')
        return getattr(self, algorithm)(text)

    def md5(self, text: str) -> str:
        return md5(text.encode()).hexdigest()

    def sha1(self, text: str) -> str:
        return sha1(text.encode()).hexdigest()

    def sha256(self, text: str) -> str:
        return sha256(text.encode()).hexdigest()

    def sha512(self, text: str) -> str:
        return sha512(text.encode()).hexdigest()

# 创建 Quart 应用实例
app = quart.Quart(__name__)

@app.route("/hash", methods=["POST"])
async def calculate_hash():
    # 从请求中获取数据
    data = await request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request data'}), 400

    # 验证请求数据
    if 'text' not in data or 'algorithm' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400

    text = data['text']
    algorithm = data['algorithm']

    # 创建哈希计算器实例
    calculator = HashCalculator()
    try:
        # 计算哈希值
        hash_value = calculator.calculate_hash(text, algorithm)
        return jsonify({'hash': hash_value}), 200
    except ValueError as e:
        # 处理无效算法错误
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # 处理其他未知错误
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
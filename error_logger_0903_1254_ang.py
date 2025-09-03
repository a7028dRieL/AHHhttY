# 代码生成时间: 2025-09-03 12:54:50
import quart
from quart import jsonify
import logging
from logging.handlers import RotatingFileHandler
import os

# 设置日志格式
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format)

# 创建日志文件处理器
handler = RotatingFileHandler('error_log.txt', maxBytes=10000, backupCount=5)
handler.setFormatter(logging.Formatter(log_format))

# 配置日志器
logger = logging.getLogger('ErrorLogger')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

app = quart.Quart(__name__)

@app.route('/log_error', methods=['POST'])
async def log_error():
    """
    Endpoint to log errors. It expects a JSON payload with 'message' and 'level' keys.
    """
    data = await quart.request.get_json()
    if 'message' not in data or 'level' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    level = getattr(logging, data['level'].upper(), logging.ERROR)
    if not isinstance(level, int):
        return jsonify({'error': 'Invalid level'}), 400
    
    logger.log(level, data['message'])
    return jsonify({'status': 'Logged'}), 200

if __name__ == '__main__':
    app.run()

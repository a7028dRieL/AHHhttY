# 代码生成时间: 2025-10-13 03:09:21
# test_result_analyzer.py

import quart
from quart import request
from quart import jsonify
import json
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义一个全局变量来存储测试结果
TEST_RESULTS = {}

app = quart.Quart(__name__)


@app.route('/upload_results', methods=['POST'])
async def upload_results():
    """
    上传测试结果接口。
    接收JSON格式的测试结果并存储。
    """
    try:
        data = await request.get_json()
        if not data or 'test_results' not in data:
            return jsonify({'error': 'Invalid data', 'message': 'Missing test results'}), 400

        # 将测试结果存储在全局变量中
        TEST_RESULTS.update(data['test_results'])
        return jsonify({'message': 'Results uploaded successfully'}), 200
    except Exception as e:
        logger.error(f"Failed to upload test results: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': 'Failed to upload test results'}), 500


@app.route('/get_results', methods=['GET'])
async def get_results():
    """
    获取测试结果接口。
    返回存储的测试结果。
    """
    try:
        # 将测试结果转换为JSON格式并返回
        return jsonify(TEST_RESULTS), 200
    except Exception as e:
        logger.error(f"Failed to retrieve test results: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': 'Failed to retrieve test results'}), 500


if __name__ == '__main__':
    # 启动服务
    app.run(debug=True, port=5000)

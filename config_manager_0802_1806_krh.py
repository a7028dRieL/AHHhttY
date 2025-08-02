# 代码生成时间: 2025-08-02 18:06:01
import quart
from quart import jsonify
import json
from pathlib import Path
import os

# 文件夹路径
CONFIG_DIR = Path('config')

# 配置文件管理器
class ConfigManager:
    def __init__(self):
        # 初始化配置文件夹
        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir()

    def load_config(self, filename: str) -> dict:
        """
        加载配置文件
        :param filename: 配置文件名
        :return: 配置内容
        """
        try:
            with open(CONFIG_DIR / filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise quart.Abort(404, '配置文件未找到')
        except json.JSONDecodeError:
            raise quart.Abort(400, '配置文件格式错误')

    def save_config(self, filename: str, config: dict) -> None:
        """
        保存配置文件
        :param filename: 配置文件名
        :param config: 配置内容
        """
        try:
            with open(CONFIG_DIR / filename, 'w') as file:
                json.dump(config, file, indent=4)
        except Exception as e:
            raise quart.Abort(500, str(e))

    def delete_config(self, filename: str) -> None:
        """
        删除配置文件
        :param filename: 配置文件名
        """
        try:
            os.remove(CONFIG_DIR / filename)
        except FileNotFoundError:
            raise quart.Abort(404, '配置文件未找到')

# Quart 应用
app = quart.Quart(__name__)

# 路由：加载配置
@app.route('/config/<string:filename>', methods=['GET'])
async def load(filename: str):
    config_manager = ConfigManager()
    config = config_manager.load_config(filename)
    return jsonify(config)

# 路由：保存配置
@app.route('/config/<string:filename>', methods=['POST'])
async def save(filename: str):
    config_manager = ConfigManager()
    config = await quart.request.get_json()
    try:
        config_manager.save_config(filename, config)
        return jsonify({'message': '配置保存成功'}), 201
    except quart.Abort as e:
        return jsonify({'error': str(e)}), e.code

# 路由：删除配置
@app.route('/config/<string:filename>', methods=['DELETE'])
async def delete(filename: str):
    config_manager = ConfigManager()
    try:
        config_manager.delete_config(filename)
        return jsonify({'message': '配置删除成功'}), 200
    except quart.Abort as e:
        return jsonify({'error': str(e)}), e.code

if __name__ == '__main__':
    app.run(debug=True)
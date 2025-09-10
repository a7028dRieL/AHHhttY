# 代码生成时间: 2025-09-11 03:22:22
import json
import os
from quart import Quart, request, jsonify
from datetime import datetime
from shutil import copy2

# 创建一个Quart应用
app = Quart(__name__)

# 数据文件路径
DATA_FILE_PATH = 'data.json'
BACKUP_FOLDER = 'backups'

# 检查备份文件夹是否存在，如果不存在则创建
if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)

@app.route('/backup', methods=['POST'])
async def backup_data():
    """
    备份当前数据。
    """
    try:
        # 读取当前数据文件
        with open(DATA_FILE_PATH, 'r') as file:
            data = json.load(file)
        # 创建备份文件名
        backup_file_name = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        backup_file_path = os.path.join(BACKUP_FOLDER, backup_file_name)
        # 复制数据文件到备份文件夹
        copy2(DATA_FILE_PATH, backup_file_path)
        return jsonify({'message': 'Backup successful', 'backup_file_path': backup_file_path}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/restore', methods=['POST'])
async def restore_data():
    """
    恢复数据到指定备份文件。
    """
    try:
        # 获取请求中的备份文件名
        backup_file_name = request.form.get('backup_file_name')
        if not backup_file_name or not backup_file_name.endswith('.json'):
            return jsonify({'error': 'Invalid backup file name'}), 400
        # 检查备份文件是否存在
        backup_file_path = os.path.join(BACKUP_FOLDER, backup_file_name)
        if not os.path.exists(backup_file_path):
            return jsonify({'error': 'Backup file not found'}), 404
        # 复制备份文件到数据文件
        copy2(backup_file_path, DATA_FILE_PATH)
        return jsonify({'message': 'Data restored successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
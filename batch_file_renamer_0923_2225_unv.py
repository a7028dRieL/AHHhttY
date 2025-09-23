# 代码生成时间: 2025-09-23 22:25:39
import os
from quart import Quart, request, jsonify

# 创建Quart应用程序
app = Quart(__name__)

# 批量文件重命名功能
@app.route('/rename', methods=['POST'])
async def rename_files():
    # 从请求中获取文件名和新的文件名列表
    try:
        files = request.json.get('files')
        new_names = request.json.get('new_names')
        
        # 错误处理：确保文件列表和新名称列表长度一致
        if not files or not new_names or len(files) != len(new_names):
            return jsonify({'error': 'Invalid input, files and new_names must be provided with the same length'}), 400
        
        # 错误处理：确保提供的路径存在
        directory = os.path.dirname(files[0])
        if not os.path.exists(directory):
            return jsonify({'error': 'Directory does not exist'}), 400

        # 重命名文件
        for old_name, new_name in zip(files, new_names):
            old_path = os.path.join(directory, old_name)
            new_path = os.path.join(directory, new_name)
            
            # 检查文件是否存在
            if not os.path.exists(old_path):
                return jsonify({'error': f'File {old_name} does not exist'}), 404
            
            # 检查新文件名是否已存在
            if os.path.exists(new_path):
                return jsonify({'error': f'File {new_name} already exists'}), 409
            
            # 执行重命名
            os.rename(old_path, new_path)
            
        # 返回成功消息
        return jsonify({'message': 'Files renamed successfully'}), 200
    
    except Exception as e:
        # 捕获并返回任何异常
        return jsonify({'error': str(e)}), 500

# 启动Quart应用程序
if __name__ == '__main__':
    app.run(debug=True)
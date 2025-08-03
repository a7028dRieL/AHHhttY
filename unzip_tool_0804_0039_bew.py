# 代码生成时间: 2025-08-04 00:39:08
import zipfile
import os
from quart import Quart, request, jsonify

# 创建一个Quart应用
app = Quart(__name__)

# 定义一个路由来处理上传并解压文件
@app.route('/unzip', methods=['POST'])
def unzip_file():
    """
    处理上传的ZIP文件并解压。
    
    参数:
    None
    
    返回:
    JSON对象，包含解压结果和错误信息（如果有）。
    """
    # 获取上传的文件
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    # 检查文件是否是ZIP格式
    if not file.filename.endswith('.zip'):
        return jsonify({'error': 'File is not a ZIP'}), 400

    try:
        # 创建临时目录
        temp_dir = 'temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # 保存上传的文件到临时目录
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)

        # 解压文件
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            
        # 清理临时文件
        os.remove(file_path)
        
        # 返回解压成功的信息
        return jsonify({'message': 'File successfully unzipped'}), 200
    except zipfile.BadZipFile:
        return jsonify({'error': 'Invalid ZIP file'}), 400
    except Exception as e:
        # 返回任何其他错误信息
        return jsonify({'error': str(e)}), 500

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
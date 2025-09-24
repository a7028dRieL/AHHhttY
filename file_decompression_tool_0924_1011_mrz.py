# 代码生成时间: 2025-09-24 10:11:10
import os
from quart import Quart, request, jsonify
from zipfile import ZipFile
from io import BytesIO
import shutil

# 创建Quart应用
app = Quart(__name__)

# API路由：用于接收压缩文件并解压
# 扩展功能模块
@app.route('/decompress', methods=['POST'])
async def decompress_file():
    # 获取上传的文件
    file = await request.files.get('file')
    
    # 检查文件是否是zip格式
    if not file.filename.endswith('.zip'):
        return jsonify({'error': 'Unsupported file format. Only .zip files are allowed.'}), 400
    
    try:
        # 将上传的文件存储在内存中
        file_content = await file.read()
        
        # 创建一个临时目录
        temp_dir = 'temp_direct'
        os.makedirs(temp_dir, exist_ok=True)
        
        # 使用ZipFile解压文件
        with ZipFile(BytesIO(file_content)) as zip_file:
            zip_file.extractall(temp_dir)
            
        # 返回成功的响应
        return jsonify({'message': 'File decompressed successfully.'}), 200
    except Exception as e:
        # 错误处理
        return jsonify({'error': str(e)}), 500
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)
        
# 运行Quart应用
if __name__ == '__main__':
    app.run(debug=True)
# 代码生成时间: 2025-08-29 20:49:29
from quart import Quart, request, jsonify
from werkzeug.utils import secure_filename
import os

# 定义一个Quart应用
app = Quart(__name__)

# 上传文件的最大尺寸限制
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# 定义允许的文件类型
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'odt', 'rtf', 'md', 'html', 'epub', 'pptx', 'ppt'}

# 检查文件扩展名是否在允许的列表中
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 路由：文件上传和转换
@app.route('/upload', methods=['POST'])
async def upload_file():
    # 检查是否有文件在请求中
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    # 如果用户没有选择文件，浏览器也会提交一个没有文件名的空部分
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        # 这里可以添加转换文档的逻辑
        # 例如，使用第三方库进行文档转换
        # 转换成功后，返回成功的响应
        return jsonify({'message': 'File uploaded and converted successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file extension'}), 400

# 启动服务器
if __name__ == '__main__':
    app.run(debug=True)
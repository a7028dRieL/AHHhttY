# 代码生成时间: 2025-09-04 22:35:09
import os
from quart import Quart, request, jsonify, abort
from werkzeug.utils import secure_filename
from pathlib import Path
import re

# 创建一个Quart应用
app = Quart(__name__)

# 定义一个正则表达式用于匹配文件名中的数字
file_number_pattern = re.compile(r"(\d+)(?!\d)")

# 定义一个函数用于生成新的文件名
def generate_new_filename(base_name, file_number, extension):
    """Generate a new filename with a specified number and extension."""
    return f"{base_name}_{file_number}{extension}"

# 定义一个函数用于重命名文件夹内的所有文件
def rename_files_in_folder(folder_path, base_name, extension):
    """Rename all files in the specified folder with the given base name and extension."""
    if not os.path.isdir(folder_path):
        abort(404, description=f"The folder {folder_path} does not exist.")

    files = os.listdir(folder_path)
    numbered_files = [file for file in files if file_number_pattern.search(file)]
    numbered_files.sort(key=lambda x: int(file_number_pattern.search(x).group(1)))

    for file in numbered_files:
        file_number = file_number_pattern.search(file).group(1)
        new_filename = generate_new_filename(base_name, file_number, extension)
        old_file_path = Path(folder_path) / file
        new_file_path = Path(folder_path) / new_filename
        os.rename(old_file_path, new_file_path)

# 创建一个路由处理POST请求
@app.route('/rename', methods=['POST'])
async def rename():
    "
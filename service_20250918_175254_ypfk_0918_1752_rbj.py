# 代码生成时间: 2025-09-18 17:52:54
import os
import shutil
from quart import Quart, jsonify, request
from datetime import datetime

# 定义一个用于文件夹整理的类
class FolderOrganizer:
    def __init__(self, root_path):
        self.root_path = root_path

    def organize(self, folder_path):
        """
        根据文件类型，将文件夹内的文件移动到指定的目录
        :param folder_path: 需要整理的文件夹路径
        """
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    self.move_file(item_path)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def move_file(self, file_path):
        """
        将文件根据扩展名移动到对应的文件夹中
        :param file_path: 文件的完整路径
        """
        file_ext = os.path.splitext(file_path)[1]
        target_folder = os.path.join(self.root_path, file_ext[1:])
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        shutil.move(file_path, target_folder)


# 创建一个Quart应用
app = Quart(__name__)

@app.route('/organize', methods=['POST'])
async def organize_folder():
    """
    处理POST请求，整理文件夹
    """
    data = await request.get_json()
    folder_path = data.get('folder_path')
    if not folder_path:
        return jsonify({'error': 'No folder path provided'}), 400

    organizer = FolderOrganizer('/path/to/organized/folder')
    response = organizer.organize(folder_path)
    if isinstance(response, tuple):
        return response
    return jsonify({'message': 'Folder organized successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
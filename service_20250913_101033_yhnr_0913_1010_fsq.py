# 代码生成时间: 2025-09-13 10:10:33
import os
import shutil
from quart import Quart, jsonify, request

# 创建Quart应用
app = Quart(__name__)

class FolderOrganizer:
    """
    文件夹整理器
    """
    def __init__(self, source_folder, target_folder):
        self.source_folder = source_folder
        self.target_folder = target_folder

    def organize(self):
        """
        整理文件夹结构
        """
        try:
            # 检查源文件夹是否存在
            if not os.path.exists(self.source_folder):
                raise FileNotFoundError(f"源文件夹不存在: {self.source_folder}")

            # 检查目标文件夹是否存在，如果不存在则创建
            if not os.path.exists(self.target_folder):
                os.makedirs(self.target_folder)

            # 遍历源文件夹中的所有文件和子文件夹
            for item in os.listdir(self.source_folder):
                item_path = os.path.join(self.source_folder, item)

                # 如果是文件夹，则递归整理
                if os.path.isdir(item_path):
                    self.organize_folder(item_path)
                # 如果是文件，则移动到目标文件夹
                else:
                    self.move_file(item_path)

            return {"status": "success", "message": "文件夹整理完成"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def organize_folder(self, folder_path):
        "
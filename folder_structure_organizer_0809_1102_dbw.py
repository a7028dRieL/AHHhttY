# 代码生成时间: 2025-08-09 11:02:33
import os
import shutil
from quart import Quart, jsonify, request, abort

# 创建Quart应用
app = Quart(__name__)

# 定义文件夹结构整理函数
def organize_folder_structure(source_path, target_path):
    """将源文件夹中的文件按照类型进行分类，并移动到目标文件夹中。

    参数:
    source_path (str): 源文件夹路径。
    target_path (str): 目标文件夹路径。
    """
    # 检查源路径是否存在
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"源路径 {source_path} 不存在。")

    # 检查目标路径是否存在，不存在则创建
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    try:
        for item in os.listdir(source_path):
            # 获取文件完整路径
            item_path = os.path.join(source_path, item)
            if os.path.isfile(item_path):
                # 根据文件扩展名分类并移动到相应的文件夹
                file_extension = item.split('.')[-1].lower()
                target_folder = os.path.join(target_path, file_extension)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                shutil.move(item_path, target_folder)
    except Exception as e:
        raise Exception(f"整理文件夹结构时发生错误：{e}")

# 定义API端点，用于触发文件夹结构整理
@app.route('/organize', methods=['POST'])
async def organize():
    """接收HTTP请求，根据请求体中的路径信息，整理文件夹结构。"""
    data = await request.get_json()
    source_path = data.get('source_path')
    target_path = data.get('target_path')

    # 参数校验
    if not source_path or not target_path:
        abort(400, description="请求体中缺少 'source_path' 或 'target_path'。")

    try:
        # 调用整理函数
        organize_folder_structure(source_path, target_path)
        return jsonify({'message': '文件夹结构整理成功。'})
    except (FileNotFoundError, Exception) as e:
        return jsonify({'error': str(e)}), 500

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
# 代码生成时间: 2025-08-27 02:48:03
from quart import Quart, request, jsonify

# 创建一个Quart应用
app = Quart(__name__)

# 用于存储当前主题的全局变量
current_theme = 'light'

# 定义主题切换的路由
# TODO: 优化性能
@app.route('/theme', methods=['POST'])
async def switch_theme():
# 增强安全性
    # 获取请求中的新主题
    new_theme = request.json.get('theme', 'light')
    
    # 检查新主题是否有效
    if new_theme not in ['light', 'dark']:
        return jsonify(error='Invalid theme'), 400
    
    # 更新当前主题
    global current_theme
    current_theme = new_theme
    
    # 返回成功响应
    return jsonify(message='Theme switched successfully', current_theme=current_theme)

# 定义获取当前主题的路由
@app.route('/theme', methods=['GET'])
async def get_current_theme():
# TODO: 优化性能
    # 返回当前主题
    return jsonify(current_theme=current_theme)

# 启动Quart应用
if __name__ == '__main__':
    app.run(debug=True)
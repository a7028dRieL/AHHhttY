# 代码生成时间: 2025-08-29 00:37:40
from quart import Quart, request, jsonify, abort
from typing import Dict, Any

# 定义一个主题切换器应用程序
app = Quart(__name__)

# 假设我们有两个可切换的主题：light 和 dark
AVAILABLE_THEMES = ["light", "dark"]

# 存储当前主题状态，实际生产环境中可能需要使用数据库或持久化存储
current_theme = "light"

@app.route('/theme', methods=['GET', 'POST'])
async def theme_endpoint() -> Dict[str, Any]:
    # GET 请求用来获取当前主题
    if request.method == 'GET':
        return jsonify({'currentTheme': current_theme})

    # POST 请求用来切换主题
    elif request.method == 'POST':
        # 获取请求体中的主题
        data = await request.get_json()
        if not data or 'theme' not in data:
            abort(400, description="Missing 'theme' in request body")

        new_theme = data['theme']
        # 检查请求的主题是否为可用主题之一
        if new_theme not in AVAILABLE_THEMES:
            abort(400, description=f"Theme '{new_theme}' is not available. Available themes are {AVAILABLE_THEMES}")

        # 更改当前主题
        global current_theme
        current_theme = new_theme
        return jsonify({'currentTheme': current_theme})

    else:
        abort(405, description="Method not allowed")

if __name__ == '__main__':
    app.run(debug=True)

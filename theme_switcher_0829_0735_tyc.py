# 代码生成时间: 2025-08-29 07:35:59
import quart
from quart import request

# 一个简单的主题切换服务
class ThemeService:
    def __init__(self):
        # 存储当前的主题
        self.current_theme = 'light'

    def get_theme(self):
        # 获取当前主题
        return self.current_theme

    def set_theme(self, theme):
        # 设置当前主题
        if theme not in ['light', 'dark']:
            raise ValueError("Invalid theme. Choose 'light' or 'dark'.")
        self.current_theme = theme
        return f"Theme set to {theme}"

# 主程序
app = quart.Quart(__name__)

@app.route('/theme/', methods=['GET'])
async def get_theme():
    # 获取当前主题
    theme_service = ThemeService()
    return quart.jsonify({'current_theme': theme_service.get_theme()})

@app.route('/theme/', methods=['POST'])
async def set_theme():
    # 设置新的主题
    theme_service = ThemeService()
    theme = request.json.get('theme')
    if theme is None:
        return quart.jsonify({'error': 'Theme not provided'})
    try:
        message = theme_service.set_theme(theme)
        return quart.jsonify({'message': message})
    except ValueError as e:
        return quart.jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # 运行Quart应用
    app.run(debug=True)
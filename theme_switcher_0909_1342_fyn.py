# 代码生成时间: 2025-09-09 13:42:01
import quart as q

# 定义一个全局变量来存储主题
current_theme = q.session.get('theme', 'light')

# 定义一个函数来切换主题
def switch_theme():
    """
    这个函数用于切换当前的主题。如果当前主题是'light'，则切换到'dark'，反之亦然。
    """
    global current_theme
    if current_theme == 'light':
        current_theme = 'dark'
    else:
        current_theme = 'light'
    q.session['theme'] = current_theme

# 创建一个Quart应用
app = q.Quart(__name__)

# 定义一个路由来展示当前主题
@app.route('/')
async def home():
    """
    这个路由用于展示当前的主题。
    """
    return f'当前主题: {current_theme}'

# 定义一个路由来切换主题
@app.route('/switch-theme')
async def switch_theme_route():
    """
    这个路由用于处理主题切换的请求。
    """
    try:
        switch_theme()
        return f'主题已切换为: {current_theme}'
    except Exception as e:
        return f'切换主题失败: {e}', 500

# 定义一个路由来设置主题
@app.route('/set-theme/<theme>')
async def set_theme(theme):
    """
    这个路由用于设置主题。
    """
    try:
        if theme not in ['light', 'dark']:
            return '无效的主题', 400
        q.session['theme'] = theme
        current_theme = theme
        return f'主题已设置为: {theme}'
    except Exception as e:
        return f'设置主题失败: {e}', 500

if __name__ == '__main__':
    app.run(debug=True)
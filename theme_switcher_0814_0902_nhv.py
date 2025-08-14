# 代码生成时间: 2025-08-14 09:02:44
from quart import Quart, request, jsonify
from functools import wraps

# 初始化Quart应用
app = Quart(__name__)

# 存储当前主题的全局变量
current_theme = 'light'

# 定义一个装饰器来切换主题
def switch_theme_theme(func):
    @wraps(func)
    async def decorated_function(*args, **kwargs):
        nonlocal current_theme
        # 检查如果是POST请求
        if request.method == 'POST':
            # 获取请求体中的新主题
            new_theme = request.get_json().get('theme')
            # 检查新主题是否有效
            if new_theme in ['light', 'dark']:
                current_theme = new_theme
                # 返回成功响应
                return jsonify({'message': 'Theme switched successfully.', 'current_theme': current_theme})
            else:
                # 如果主题无效，返回错误响应
                return jsonify({'error': 'Invalid theme.'}), 400
        # 如果不是POST请求，返回当前主题
        return jsonify({'current_theme': current_theme})
    return decorated_function

# 使用装饰器创建一个路由来处理主题切换请求
@app.route('/theme', methods=['GET', 'POST'])
@switch_theme_theme
async def theme():
    # 这个函数被装饰器装饰后，会处理主题切换逻辑
    pass

# 定义一个路由来测试当前主题
@app.route('/test_theme')
async def test_theme():
    # 返回当前主题作为响应
    return jsonify({'current_theme': current_theme})

if __name__ == '__main__':
    # 运行Quart应用
    app.run()
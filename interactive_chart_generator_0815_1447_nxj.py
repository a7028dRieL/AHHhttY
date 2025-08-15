# 代码生成时间: 2025-08-15 14:47:52
import quart

from quart import jsonify
from quart import request
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import base64

# 设置静态文件路径
STATIC_DIR = './static'

# 创建 Quart 应用
app = quart.Quart(__name__)

"""
交互式图表生成器
"""
@app.route('/chart', methods=['GET', 'POST'])
async def chart():
    """
    这个视图负责接收数据，生成图表，并返回图表的 HTML 代码。
    参数：
    - GET 请求用于返回表单页面。
    - POST 请求用于处理表单提交的数据，并生成图表。
    """
    if request.method == 'GET':
        # 返回表单页面
        return quart.render_template('form.html')
    else:
        # 处理 POST 请求
        try:
            # 获取请求数据
            df = pd.DataFrame(request.form.to_dict())
            # 生成图表
            fig = px.line(df)
            # 将图表保存为 HTML 文件
            html = plot(fig, filename='temp.html', auto_open=False)
            # 将 HTML 文件转换为 base64 编码的字符串
            html_b64 = base64.b64encode(html.encode()).decode()
            # 返回图表的 HTML 代码
            return jsonify({'chart_html': 'data:text/html;base64,' + html_b64})
        except Exception as e:
            # 错误处理
            return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # 运行应用
    app.run(debug=True)
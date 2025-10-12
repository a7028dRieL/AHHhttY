# 代码生成时间: 2025-10-12 17:17:52
import quart
from quart import request

# 导入所需的库
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

# 设置应用
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义交互式图表生成器路由
@app.route('/chart')
async def chart_generator():
    # 获取请求参数
    data = request.args.get('data')
    if not data:
        return 'Please provide data in the format: key1=value1&key2=value2...'

    # 将请求参数转换为字典
    params = dict(param.split('=') for param in data.split('&'))

    # 创建图表
    try:
        # 假设params中包含'x'和'y'键用于图表的X轴和Y轴
        df = px.data.iris()  # 使用一个示例数据集
        chart = px.scatter(df, x=params.get('x', 'sepal_length'), y=params.get('y', 'sepal_width'))
        # 将图表转换为HTML
        chart_div = chart.to_html(full_html=False)
    except Exception as e:
        # 错误处理
        return f'An error occurred: {e}'

    # 返回图表HTML
    return html.Div([dcc.Graph(figure=chart), html.Div(chart_div)])

# 定义根路由
@app.route('/')
async def index():
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H1("Interactive Chart Generator"), className="mb-2"),
            ]),
            dbc.Row([
                dbc.Col(html.Div("Enter your parameters as key=value&key2=value2... 
For example: x=sepal_length&y=sepal_width"), className="mb-2"),
            ]),
            dbc.Row([
                dbc.Col(dbc.Form([
                    dbc.FormGroup([
                        dbc.Label("Data Parameters", className="form-label"),
                        dbc.Input(type="text", placeholder="x=sepal_length&y=sepal_width", id="data-input"),
                    ]),
                    dbc.Button("Generate Chart", color="primary", className="mt-2", id="submit-button"),
                ]), className="mb-3"),
            ]),
            dbc.Row([
                dbc.Col(dcc.Location(id="url", refresh=False), className="mb-3"),
            ]),
            dbc.Row([
                dbc.Col(html.Div(id="page-content")),
            ]),
        ]),
    ])

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)

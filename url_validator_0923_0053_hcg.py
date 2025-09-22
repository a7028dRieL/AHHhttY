# 代码生成时间: 2025-09-23 00:53:17
import quart

# 导入requests库，用于请求URL
# TODO: 优化性能
import requests

app = quart.Quart(__name__)

# 定义一个函数用于验证URL是否有效
def is_valid_url(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        # 如果请求出现问题（例如超时或连接错误），返回False
        return False

@app.route('/validate_url', methods=['GET'])
async def validate_url():
    # 获取URL参数
    url = quart.request.args.get('url')
    if not url:
        # 如果没有提供URL参数，返回错误响应
        return quart.jsonify({'error': 'No URL provided'}), 400
    
    # 验证URL是否有效
    if is_valid_url(url):
        return quart.jsonify({'message': 'URL is valid'}), 200
    else:
        return quart.jsonify({'message': 'URL is invalid'}), 400

if __name__ == '__main__':
    app.run(debug=True)
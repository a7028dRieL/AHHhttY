# 代码生成时间: 2025-09-22 11:10:08
from quart import Quart, render_template, send_from_directory, request
import os
import json
import datetime

# 初始化Quart应用
app = Quart(__name__)

# 测试报告存储路径
TEST_REPORTS_PATH = 'test_reports'

# 确保测试报告存储路径存在
if not os.path.exists(TEST_REPORTS_PATH):
    os.makedirs(TEST_REPORTS_PATH)

@app.route('/report', methods=['GET', 'POST'])
async def generate_test_report():
    """
    生成测试报告的路由
    
    GET 请求返回测试报告生成表单
    POST 请求处理表单数据，生成测试报告
    """
    if request.method == 'GET':
        # 返回测试报告生成表单页面
        return await render_template('generate_test_report.html')
    else:
        # 处理表单数据，生成测试报告
        try:
            form_data = await request.form
            report_name = form_data['report_name']
            report_content = form_data['report_content']
            
            # 确保报告名称和内容不为空
            if not report_name or not report_content:
                return 'Report name and content are required', 400
            
            # 生成报告文件路径
            report_path = os.path.join(TEST_REPORTS_PATH, f'{report_name}.json')
            
            # 将报告内容写入文件
            with open(report_path, 'w') as f:
                json.dump(json.loads(report_content), f, indent=4)
            
            # 返回报告生成成功消息
            return f'Report {report_name} generated successfully', 200
        except Exception as e:
            # 返回错误信息
            return f'Error generating report: {str(e)}', 500

@app.route('/report/<filename>', methods=['GET'])
async def get_test_report(filename):
    """
    获取测试报告的路由
    
    根据报告名称返回相应的测试报告文件
    """
    try:
        # 构建报告文件完整路径
        report_path = os.path.join(TEST_REPORTS_PATH, filename)
        
        # 发送报告文件
        return await send_from_directory(TEST_REPORTS_PATH, filename)
    except FileNotFoundError:
        # 如果文件不存在，返回404错误
        return 'Report file not found', 404
    except Exception as e:
        # 返回其他错误信息
        return f'Error retrieving report: {str(e)}', 500

# 运行Quart应用
if __name__ == '__main__':
    app.run(debug=True)
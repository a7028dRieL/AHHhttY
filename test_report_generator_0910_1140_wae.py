# 代码生成时间: 2025-09-10 11:40:17
import quart
from quart import request, jsonify
import json
import os
import datetime

# 定义测试报告生成器类
class TestReportGenerator:
    def __init__(self):
        self.template = """<html>\
<head><title>Test Report</title></head>\
<body>\
<h1>Test Report</h1>\
<div>\
Test Date: {test_date}\
<h2>Test Results</h2>\
<table border="1">""
        <caption>Test Results Table</caption>""
        <tr>""
        <th>Test Case ID</th>""
        <th>Test Case Name</th>""
        <th>Test Result</th>""
        <th>Test Description</th>""
        </tr>""
        {test_results}""
        </table>""
        </div>""
</body>\
</html>"""

    def generate_report(self, test_results):
        """根据测试结果生成测试报告"""
        test_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_results_html = ""
        for result in test_results:
            test_results_html += "<tr>
"
            test_results_html += f"<td>{result['test_case_id']}</td>
"
            test_results_html += f"<td>{result['test_case_name']}</td>
"
            test_results_html += f"<td>{result['test_result']}</td>
"
            test_results_html += f"<td>{result['test_description']}</td>
"
            test_results_html += "</tr>
"

        report_html = self.template.format(test_date=test_date, test_results=test_results_html)
        return report_html

# 创建Quart应用
app = quart.Quart(__name__)

# 定义生成测试报告的路由
@app.route('/test-report', methods=['POST'])
async def generate_test_report():
    try:
        # 获取请求体中的测试结果
        data = await request.get_json()
        test_results = data.get('test_results')

        # 检查测试结果是否有效
        if not test_results:
            return jsonify({'error': 'Invalid test results'}), 400

        # 生成测试报告
        report_generator = TestReportGenerator()
        report_html = report_generator.generate_report(test_results)

        # 保存测试报告到文件
        report_filename = f"test_report_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.html"
        with open(report_filename, 'w') as f:
            f.write(report_html)

        # 返回测试报告文件名
        return jsonify({'report_filename': report_filename}), 200

    except Exception as e:
        # 返回错误信息
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
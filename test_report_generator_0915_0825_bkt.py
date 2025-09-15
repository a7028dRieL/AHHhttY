# 代码生成时间: 2025-09-15 08:25:47
import quart
from quart import jsonify
import json
import os

# 定义TestReportGenerator类
class TestReportGenerator:
    def __init__(self, report_dir):
        """
        初始化报告生成器
        :param report_dir: 测试报告的存储目录
        """
        self.report_dir = report_dir

    def generate_report(self, test_results):
        """
        生成测试报告
        :param test_results: 测试结果列表
        :return: 测试报告的文件路径
        """
        report_file = os.path.join(self.report_dir, 'test_report.json')
        with open(report_file, 'w') as f:
            json.dump(test_results, f, indent=4)
        return report_file

# 创建Quart应用
app = quart.Quart(__name__)

@app.route('/generate-report', methods=['POST'])
async def generate_test_report():
    """
    生成测试报告的接口
    :return: 测试报告的文件路径
    """
    try:
        # 获取请求体中的测试结果
        test_results = await quart.request.get_json()
        if not test_results:
            return jsonify({'error': 'Invalid test results'}), 400

        # 创建报告生成器实例
        report_generator = TestReportGenerator('reports')

        # 生成测试报告
        report_file = report_generator.generate_report(test_results)

        # 返回报告文件路径
        return jsonify({'report_file': report_file}), 200
    except Exception as e:
        # 处理异常
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
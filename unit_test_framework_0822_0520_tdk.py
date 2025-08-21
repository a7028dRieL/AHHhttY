# 代码生成时间: 2025-08-22 05:20:35
import unittest
from quart import Quart, jsonify

# 创建一个Quart应用
app = Quart(__name__)

# 示例函数，用于测试
@app.route("/example")
def example():
    return {"message": "Hello, World!"}


class TestExample(unittest.TestCase):
    """测试/example路由的单元测试类"""
    def test_example(self):
        """测试/example路由返回的数据是否正确"""
        with app.test_client() as client:
            response = client.get("/example")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"message": "Hello, World!"})


if __name__ == '__main__':
    # 运行单元测试
    unittest.main()
    # 启动Quart应用
    app.run(debug=True)
# 代码生成时间: 2025-10-10 02:12:28
import quart
from quart.testing import QuartClient
import unittest

# 创建一个简单的Quart应用
app = quart.Quart(__name__)


def create_app():
    """创建Quart应用实例"""
    return app

@app.route("/")
async def index():
    """首页路由"""
    return "Hello, Quart!"

# 单元测试类
class TestQuartApp(unittest.IsolatedAsyncioTestCase):
    """Quart应用的单元测试"""
    async def asyncSetUp(self):
        """异步设置测试环境"""
        self.app = create_app()
        self.client = QuartClient(self.app)

    async def asyncTearDown(self):
        """异步清理测试环境"""
        await self.client.close()

    async def test_index(self):
        """测试首页路由"""
        response = await self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Hello, Quart!")

# 运行单元测试
if __name__ == '__main__':
    unittest.main()
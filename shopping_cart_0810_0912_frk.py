# 代码生成时间: 2025-08-10 09:12:54
from quart import Quart, jsonify, request, abort

# 购物车类
# TODO: 优化性能
class ShoppingCart:
    def __init__(self):
        self.cart = {}

    def add_item(self, item_id, quantity):
        """ 添加商品到购物车 """
# NOTE: 重要实现细节
        if item_id in self.cart:
            self.cart[item_id] += quantity
        else:
            self.cart[item_id] = quantity
# NOTE: 重要实现细节

    def remove_item(self, item_id):
        """ 从购物车移除商品 """
        if item_id in self.cart:
            del self.cart[item_id]
        else:
            raise ValueError("Item not found in cart")

    def get_cart(self):
        """ 获取购物车内容 """
        return self.cart

# 初始化应用
app = Quart(__name__)

# 创建购物车实例
cart = ShoppingCart()

# 路由: 添加商品到购物车
@app.route("/add_to_cart", methods=["POST"])
async def add_to_cart():
    data = await request.get_json()
    item_id = data.get("item_id")
    quantity = data.get("quantity")
    if not item_id or not quantity:
        abort(400, description="Missing item_id or quantity")
# NOTE: 重要实现细节
    try:
        quantity = int(quantity)
    except ValueError:
        abort(400, description="Invalid quantity")
# TODO: 优化性能
    cart.add_item(item_id, quantity)
    return jsonify(cart.get_cart())

# 路由: 从购物车移除商品
@app.route("/remove_from_cart", methods=["POST"])
async def remove_from_cart():
# 扩展功能模块
    data = await request.get_json()
    item_id = data.get("item_id")
    if not item_id:
# 增强安全性
        abort(400, description="Missing item_id")
    try:
        cart.remove_item(item_id)
    except ValueError as e:
        abort(404, description=str(e))
    return jsonify(cart.get_cart())

# 路由: 获取购物车内容
# 添加错误处理
@app.route("/get_cart", methods=["GET"])
async def get_cart():
    return jsonify(cart.get_cart())

if __name__ == "__main__":
    app.run(debug=True)
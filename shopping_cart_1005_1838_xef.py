# 代码生成时间: 2025-10-05 18:38:50
import quart

# ShoppingCart 类用于管理购物车
class ShoppingCart:
    def __init__(self):
        self.items = {}

    # 添加商品到购物车
    def add_item(self, item_id, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if item_id not in self.items:
            self.items[item_id] = 0
        self.items[item_id] += quantity
        return self.items

    # 从购物车移除商品
    def remove_item(self, item_id, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if item_id in self.items and self.items[item_id] >= quantity:
            self.items[item_id] -= quantity
            if self.items[item_id] == 0:
                del self.items[item_id]
            return self.items
        else:
            raise ValueError("Item not in cart or quantity exceeds the available quantity")

    # 获取购物车中商品的总数
    def get_total_items(self):
        return sum(self.items.values())

    # 获取购物车中的所有商品
    def get_items(self):
        return self.items

# 创建一个 Quart 应用
app = quart.Quart(__name__)

# 创建一个购物车实例
cart = ShoppingCart()

# 路由和视图函数
@app.route('/add_item/<int:item_id>/<int:quantity>', methods=['POST'])
async def add_item(item_id, quantity):
    try:
        cart.add_item(item_id, quantity)
        return quart.jsonify({'message': 'Item added', 'cart': cart.get_items()})
    except ValueError as e:
        return quart.jsonify({'error': str(e)}), 400

@app.route('/remove_item/<int:item_id>/<int:quantity>', methods=['POST'])
async def remove_item(item_id, quantity):
    try:
        cart.remove_item(item_id, quantity)
        return quart.jsonify({'message': 'Item removed', 'cart': cart.get_items()})
    except ValueError as e:
        return quart.jsonify({'error': str(e)}), 400

@app.route('/cart', methods=['GET'])
async def get_cart():
    return quart.jsonify({'cart': cart.get_items(), 'total_items': cart.get_total_items()})

# 启动应用
if __name__ == '__main__':
    app.run(debug=True)
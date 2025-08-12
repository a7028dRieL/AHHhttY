# 代码生成时间: 2025-08-12 11:28:41
import quart

# 购物车类
class ShoppingCart:
    def __init__(self):
        # 初始化购物车，使用字典存储商品和数量
        self.items = {}

    # 添加商品到购物车
    def add_item(self, item, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    # 从购物车移除商品
    def remove_item(self, item, quantity):
        if item in self.items:
            if quantity >= self.items[item]:
                del self.items[item]
            else:
                self.items[item] -= quantity
        else:
            raise KeyError("Item does not exist in the shopping cart")

    # 获取购物车中所有商品的总价格
    def get_total_price(self, prices):
        total = 0
        for item, quantity in self.items.items():
            if item in prices:
                total += prices[item] * quantity
            else:
                raise KeyError("Price for item does not exist")
        return total

# Quart应用
app = quart.Quart(__name__)

# 模拟商品价格字典
prices = {"apple": 2, "banana": 1.5, "cherry": 3}

# 购物车实例
cart = ShoppingCart()

# 添加商品到购物车的API
@app.route('/add-item', methods=['POST'])
async def add_item():
    data = await quart.request.get_json()
    item = data.get('item')
    quantity = data.get('quantity')
    try:
        cart.add_item(item, quantity)
        return quart.jsonify({'message': f"Added {quantity} {item}(s) to the cart"}), 200
    except (ValueError, KeyError) as e:
        return quart.jsonify({'error': str(e)}), 400

# 从购物车移除商品的API
@app.route('/remove-item', methods=['POST'])
async def remove_item():
    data = await quart.request.get_json()
    item = data.get('item')
    quantity = data.get('quantity')
    try:
        cart.remove_item(item, quantity)
        return quart.jsonify({'message': f"Removed {quantity} {item}(s) from the cart"}), 200
    except (KeyError) as e:
        return quart.jsonify({'error': str(e)}), 400

# 获取购物车总价的API
@app.route('/get-total-price', methods=['GET'])
async def get_total_price():
    try:
        total = cart.get_total_price(prices)
        return quart.jsonify({'total_price': total}), 200
    except KeyError as e:
        return quart.jsonify({'error': str(e)}), 400

# 运行Quart应用
if __name__ == '__main__':
    app.run(debug=True)
# 代码生成时间: 2025-08-03 15:09:23
# inventory_management.py

from quart import Quart, jsonify, request
from typing import List, Dict

# 定义库存项类
class InventoryItem:
    def __init__(self, item_id: int, name: str, quantity: int):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return f"{self.item_id} - {self.name}, Quantity: {self.quantity}"

# 定义库存管理系统类
class InventoryManagement:
    def __init__(self):
        self.items = {}

    def add_or_update_item(self, item_id: int, name: str, quantity: int) -> bool:
        # 添加或更新库存项
        if item_id in self.items:
            self.items[item_id].quantity += quantity
            return True
        else:
            self.items[item_id] = InventoryItem(item_id, name, quantity)
            return True

    def remove_item(self, item_id: int) -> bool:
        # 移除库存项
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False

    def get_item(self, item_id: int) -> InventoryItem:
        # 获取库存项
        return self.items.get(item_id, None)

    def list_all_items(self) -> List[InventoryItem]:
        # 列出所有库存项
        return list(self.items.values())

# 创建Quart应用
app = Quart(__name__)
inventory = InventoryManagement()

# API路由 - 添加或更新库存项
@app.route('/inventory', methods=['POST'])
async def add_or_update_inventory():
    data = await request.get_json()
    if not data or 'item_id' not in data or 'name' not in data or 'quantity' not in data:
        return jsonify({'error': 'Missing data'}), 400
    item_id = data['item_id']
    name = data['name']
    quantity = data['quantity']
    if inventory.add_or_update_item(item_id, name, quantity):
        return jsonify({'message': 'Item added/updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to add/update item'}), 500

# API路由 - 移除库存项
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
async def remove_inventory(item_id: int):
    if inventory.remove_item(item_id):
        return jsonify({'message': 'Item removed successfully'}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

# API路由 - 获取库存项
@app.route('/inventory/<int:item_id>', methods=['GET'])
async def get_inventory(item_id: int):
    item = inventory.get_item(item_id)
    if item:
        return jsonify({'item_id': item.item_id, 'name': item.name, 'quantity': item.quantity}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

# API路由 - 列出所有库存项
@app.route('/inventory', methods=['GET'])
async def list_inventory():
    items = inventory.list_all_items()
    if items:
        return jsonify([{'item_id': item.item_id, 'name': item.name, 'quantity': item.quantity} for item in items]), 200
    else:
        return jsonify({'message': 'No items found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
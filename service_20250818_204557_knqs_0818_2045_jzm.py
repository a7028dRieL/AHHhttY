# 代码生成时间: 2025-08-18 20:45:57
# inventory管理系统.py
# 库存管理系统，使用Quart框架实现RESTful API

from quart import Quart, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound

app = Quart(__name__)

# 模拟数据库
inventory = {
    "items": [
        {
            "id": 1,
            "name": "Widget",
            "quantity": 50
        },
        {
            "id": 2,
            "name": "Gadget",
            "quantity": 30
        }
    ]
}

# 路由：获取所有库存项
@app.route('/inventory', methods=['GET'])
async def get_inventory():
    """
    返回库存中所有的项目
    """
    return jsonify(inventory['items'])

# 路由：获取单个库存项
@app.route('/inventory/<int:item_id>', methods=['GET'])
async def get_item(item_id):
    """
    根据ID返回单个库存项
    """
    item = next((item for item in inventory['items'] if item['id'] == item_id), None)
    if not item:
        raise NotFound(description=f"Item with id {item_id} not found")
    return jsonify(item)

# 路由：添加库存项
@app.route('/inventory', methods=['POST'])
async def add_item():
    """
    添加新的库存项
    """
    data = await request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        raise BadRequest(description="Missing 'name' or 'quantity'")
    item = {
        "id": max(item['id'] for item in inventory['items']) + 1 if inventory['items'] else 1,
        "name": data['name'],
        "quantity": data['quantity']
    }
    inventory['items'].append(item)
    return jsonify(item), 201

# 路由：更新库存项
@app.route('/inventory/<int:item_id>', methods=['PUT'])
async def update_item(item_id):
    """
    更新指定ID的库存项
    """
    item = next((item for item in inventory['items'] if item['id'] == item_id), None)
    if not item:
        raise NotFound(description=f"Item with id {item_id} not found")
    data = await request.get_json()
    if 'name' in data:
        item['name'] = data['name']
    if 'quantity' in data:
        item['quantity'] = data['quantity']
    return jsonify(item)

# 路由：删除库存项
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
async def delete_item(item_id):
    """
    删除指定ID的库存项
    """
    global inventory
    item = next((item for item in inventory['items'] if item['id'] == item_id), None)
    if not item:
        raise NotFound(description=f"Item with id {item_id} not found")
    inventory['items'] = [item for item in inventory['items'] if item['id'] != item_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
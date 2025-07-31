# 代码生成时间: 2025-08-01 05:27:45
from quart import Quart, jsonify, request, abort

# 定义库存管理系统
app = Quart(__name__)

# 模拟数据库，存储库存数据
inventory_db = {
    'items': [
        {'id': 1, 'name': 'Apple', 'quantity': 50},
        {'id': 2, 'name': 'Banana', 'quantity': 30},
        {'id': 3, 'name': 'Orange', 'quantity': 20}
    ]
}

# 获取所有库存项
@app.route('/inventory', methods=['GET'])
def get_inventory():
    """
    获取所有库存项的接口。
    返回值：
    - 库存项列表的JSON表示。
    """
    return jsonify(inventory_db['items'])

# 获取单个库存项
@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    """
    根据ID获取单个库存项的接口。
    参数：
    - item_id: 库存项的ID。
    返回值：
    - 单个库存项的JSON表示。
    """
    item = next((item for item in inventory_db['items'] if item['id'] == item_id), None)
    if item is None:
        abort(404)
    return jsonify(item)

# 添加库存项
@app.route('/inventory', methods=['POST'])
def add_inventory_item():
    """
    添加新库存项的接口。
    参数：
    - JSON格式的库存项数据。
    返回值：
    - 新添加的库存项的JSON表示。
    """
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        abort(400)
    new_item = {'id': max([item['id'] for item in inventory_db['items']] + [0]) + 1,
                'name': data['name'],
                'quantity': data['quantity']}
    inventory_db['items'].append(new_item)
    return jsonify(new_item), 201

# 更新库存项
@app.route('/inventory/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    """
    根据ID更新库存项的接口。
    参数：
    - item_id: 库存项的ID。
    - JSON格式的更新数据。
    返回值：
    - 更新后的库存项的JSON表示。
    """
    item = next((item for item in inventory_db['items'] if item['id'] == item_id), None)
    if item is None:
        abort(404)

    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        abort(400)

    item['name'] = data['name']
    item['quantity'] = data['quantity']
    return jsonify(item)

# 删除库存项
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    """
    根据ID删除库存项的接口。
    参数：
    - item_id: 库存项的ID。
    返回值：
    - 被删除的库存项的JSON表示。
    """
    item = next((item for item in inventory_db['items'] if item['id'] == item_id), None)
    if item is None:
        abort(404)
    inventory_db['items'].remove(item)
    return jsonify(item)

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
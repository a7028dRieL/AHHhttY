# 代码生成时间: 2025-09-24 00:49:43
# message_notification.py
# A simple notification system using Quart framework.

from quart import Quart, jsonify, request
from datetime import datetime

app = Quart(__name__)

# In-memory storage for notifications
notifications = []

# Route to send a notification
@app.route("/send", methods=["POST"])
async def send_notification():
    data = await request.get_json()
    if not data or 'message' not in data:
        return jsonify(error="Missing required 'message' field"), 400
# 扩展功能模块

    # Validate message format
    if not isinstance(data['message'], str):
        return jsonify(error="'message' field must be a string"), 400
    
    # Create notification entry
    notification = {
        "timestamp": datetime.utcnow().isoformat(),
        "message": data['message']
    }
    notifications.append(notification)
# 改进用户体验
    return jsonify(notification), 201

# Route to retrieve all notifications
@app.route("/notifications", methods=["GET"])
async def get_notifications():
    return jsonify(notifications), 200

# Route to clear all notifications
@app.route("/clear", methods=["DELETE"])
async def clear_notifications():
    global notifications
    notifications.clear()
    return jsonify({}), 204

if __name__ == '__main__':
# NOTE: 重要实现细节
    app.run(debug=True)
# 代码生成时间: 2025-10-08 20:45:54
import quart
from quart import jsonify, request

# 定义成就系统类
class AchievementSystem:
    def __init__(self):
        # 初始化成就列表
        self.achievements = []
        # 初始化用户成就记录
        self.user_achievements = {}

    def add_achievement(self, achievement):
        """添加新的成就到系统中

        :param achievement: 成就对象，包含id和description
        """
        self.achievements.append(achievement)

    def unlock_achievement(self, user_id, achievement_id):
        """解锁用户的成就

        :param user_id: 用户ID
        :param achievement_id: 成就ID
        :return: 成功或失败的响应
        """
        if achievement_id not in [a['id'] for a in self.achievements]:
            return {"error": "Achievement not found"}

        if user_id in self.user_achievements and achievement_id in self.user_achievements[user_id]:
            return {"error": "Achievement already unlocked"}

        self.user_achievements.setdefault(user_id, []).append(achievement_id)
        return {"success": True}

    def get_user_achievements(self, user_id):
        """获取用户的成就列表

        :param user_id: 用户ID
        :return: 用户的成就列表
        """
        return self.user_achievements.get(user_id, [])

# 创建Quart应用
app = quart.Quart(__name__)

# 创建成就系统实例
achievement_system = AchievementSystem()

# 初始化一些成就
achievements = [
    {"id": 1, "description": "First Login"},
    {"id": 2, "description": "Post 10 Messages"},
    {"id": 3, "description": "Follow 5 People"},
]
for achievement in achievements:
    achievement_system.add_achievement(achievement)

# API：解锁成就
@app.route('/unlock', methods=['POST'])
async def unlock_achievement_api():
    data = await request.get_json()
    user_id = data.get('user_id')
    achievement_id = data.get('achievement_id')
    if not user_id or not achievement_id:
        return jsonify({'error': 'Missing user_id or achievement_id'}), 400
    result = achievement_system.unlock_achievement(user_id, achievement_id)
    return jsonify(result)

# API：获取用户成就
@app.route('/achievements', methods=['GET'])
async def get_user_achievements_api():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400
    achievements = achievement_system.get_user_achievements(user_id)
    return jsonify({'achievements': achievements})

if __name__ == '__main__':
    app.run(debug=True)
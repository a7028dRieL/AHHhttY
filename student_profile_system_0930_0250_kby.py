# 代码生成时间: 2025-09-30 02:50:25
import quart

# 学生画像系统
class StudentProfileSystem:
    def __init__(self):
        # 初始化学生数据
        self.students = {}

    def add_student(self, student_id, student_info):
        """添加学生信息"""
        if student_id in self.students:
            raise ValueError("Student with this ID already exists.")
        self.students[student_id] = student_info
        return "Student added successfully."

    def get_student(self, student_id):
        """获取学生信息"""
        if student_id not in self.students:
            raise ValueError("Student not found.")
        return self.students[student_id]

    def update_student(self, student_id, student_info):
        """更新学生信息"""
        if student_id not in self.students:
            raise ValueError("Student not found.")
        self.students[student_id].update(student_info)
        return "Student updated successfully."

    def delete_student(self, student_id):
        """删除学生信息"""
        if student_id not in self.students:
            raise ValueError("Student not found.")
        del self.students[student_id]
        return "Student deleted successfully."

# 启动Quart服务
app = quart.Quart(__name__)

# 实例化学生画像系统
student_profile_system = StudentProfileSystem()

# 添加学生信息的路由
@app.route('/add_student/<student_id>', methods=['POST'])
async def add_student(student_id):
    student_info = await quart.request.get_json()
    try:
        result = student_profile_system.add_student(student_id, student_info)
        return quart.jsonify({'result': result}), 200
    except ValueError as e:
        return quart.jsonify({'error': str(e)}), 400

# 获取学生信息的路由
@app.route('/get_student/<student_id>', methods=['GET'])
async def get_student(student_id):
    try:
        student_info = student_profile_system.get_student(student_id)
        return quart.jsonify(student_info), 200
    except ValueError as e:
        return quart.jsonify({'error': str(e)}), 400

# 更新学生信息的路由
@app.route('/update_student/<student_id>', methods=['POST'])
async def update_student(student_id):
    student_info = await quart.request.get_json()
    try:
        result = student_profile_system.update_student(student_id, student_info)
        return quart.jsonify({'result': result}), 200
    except ValueError as e:
        return quart.jsonify({'error': str(e)}), 400

# 删除学生信息的路由
@app.route('/delete_student/<student_id>', methods=['DELETE'])
async def delete_student(student_id):
    try:
        result = student_profile_system.delete_student(student_id)
        return quart.jsonify({'result': result}), 200
    except ValueError as e:
        return quart.jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
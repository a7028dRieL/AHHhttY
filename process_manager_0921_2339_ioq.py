# 代码生成时间: 2025-09-21 23:39:35
import quart
import psutil
from quart import jsonify

# 进程管理器 Flask 应用
app = quart.Quart(__name__)

# 获取系统中所有进程的信息
@app.route('/processes', methods=['GET'])
def get_processes():
    try:
        # 获取所有进程信息
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            processes.append(proc.info)
        return jsonify(processes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 启动或停止进程
@app.route('/process', methods=['POST'])
def manage_process():
    data = request.json
    pid = data.get('pid')
    action = data.get('action')
    try:
        if not pid:
            return jsonify({'error': 'Process ID is required'}), 400
        proc = psutil.Process(pid)
        if action == 'start':
            # 启动进程（实际操作根据需求进行修改）
            pass
        elif action == 'stop':
            # 停止进程
            proc.terminate()
            return jsonify({'message': 'Process terminated successfully'})
        else:
            return jsonify({'error': 'Invalid action'}), 400
    except psutil.NoSuchProcess:
        return jsonify({'error': 'Process not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
# 代码生成时间: 2025-08-02 14:25:30
import quart
from quart import jsonify
import subprocess
import psutil
import sys

# 定义进程管理器类
class ProcessManager:
    def __init__(self):
        pass

    # 获取所有进程信息
    def get_processes(self):
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                processes.append({'pid': proc.info['pid'], 'name': proc.info['name']})
            return jsonify(processes)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # 启动一个进程
    def start_process(self, command):
        try:
            process = subprocess.Popen(command, shell=True)
            return jsonify({'pid': process.pid, 'message': 'Process started successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # 终止一个进程
    def terminate_process(self, pid):
        try:
            process = psutil.Process(pid)
            process.terminate()
            return jsonify({'message': 'Process terminated successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# 创建Quart应用
app = quart.Quart(__name__)

# 定义路由和视图函数
@app.route('/processes', methods=['GET'])
async def list_processes():
    return ProcessManager().get_processes()

@app.route('/start/<command>', methods=['POST'])
async def start_process(command):
    return ProcessManager().start_process(command)

@app.route('/terminate/<pid>', methods=['POST'])
async def terminate_process(pid):
    return ProcessManager().terminate_process(int(pid))

if __name__ == '__main__':
    # 运行Quart应用
    app.run(host='0.0.0.0', port=5000)
# 代码生成时间: 2025-09-20 02:27:16
import psutil
from quart import Quart, jsonify
# 扩展功能模块

# 创建 Quart 应用
app = Quart(__name__)

# 获取 CPU 使用率的视图
@app.route("/cpu_usage")
async def get_cpu_usage():
    """返回当前 CPU 使用率"""
    try:
        # 获取 CPU 使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        return jsonify({"cpu_usage": cpu_usage})
    except Exception as e:
        # 错误处理
# NOTE: 重要实现细节
        return jsonify({"error": str(e)}), 500

# 获取内存使用的视图
# 改进用户体验
@app.route("/memory_usage")
async def get_memory_usage():
    """返回当前内存使用情况"""
    try:
        memory = psutil.virtual_memory()
# 优化算法效率
        return jsonify({
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percent": memory.percent
        })
    except Exception as e:
        # 错误处理
        return jsonify({"error": str(e)}), 500

# 获取磁盘使用情况的视图
@app.route("/disk_usage")
# TODO: 优化性能
async def get_disk_usage():
    """返回当前磁盘使用情况"""
    try:
        disk_usage = psutil.disk_usage('/')  # 可以修改为其他路径
        return jsonify({
            "total": disk_usage.total,
            "used": disk_usage.used,
            "free": disk_usage.free,
            "percent": disk_usage.percent
        })
    except Exception as e:
        # 错误处理
        return jsonify({"error": str(e)}), 500

# 获取网络使用情况的视图
# 添加错误处理
@app.route("/network_usage")
async def get_network_usage():
    """返回当前网络使用情况"""
    try:
        network_io = psutil.net_io_counters()
        return jsonify({
            "bytes_sent": network_io.bytes_sent,
            "bytes_recv": network_io.bytes_recv
# TODO: 优化性能
        })
    except Exception as e:
        # 错误处理
# TODO: 优化性能
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 运行应用
    app.run(debug=True)
# NOTE: 重要实现细节
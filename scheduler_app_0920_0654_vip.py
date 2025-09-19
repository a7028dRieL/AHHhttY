# 代码生成时间: 2025-09-20 06:54:39
import asyncio
import logging
from quart import Quart, jsonify
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建Quart应用
app = Quart(__name__)

# 创建定时任务调度器
scheduler = AsyncIOScheduler(jobstores={"default": MemoryJobStore()},
                          executors={"default": AsyncIOExecutor()},
                           event_loop=asyncio.get_event_loop())

# 定时任务示例
def job_function():
    logger.info("定时任务执行")
    # 这里可以添加实际的定时任务逻辑
    # 例如：执行数据库操作、发送邮件通知等

# 添加定时任务
scheduler.add_job(job_function, trigger=IntervalTrigger(seconds=10))

# 启动定时任务调度器
@scheduler.startup
def scheduler_start():
    scheduler.start()

# 关闭定时任务调度器
@scheduler.shutdown
def scheduler_shutdown():
    scheduler.shutdown()

# Quart应用启动时添加定时任务
@app.before_first_request
def before_first_request():
    scheduler_start()

# Quart应用关闭时关闭定时任务调度器
@app.teardown_appcontext
def teardown_appcontext(exception):
    scheduler_shutdown()
    if exception:
        logger.error(exception)

# 测试接口
@app.route("/test")
async def test():
    return jsonify({"message": "Hello, Quartz!"})

if __name__ == '__main__':
    app.run()

# 代码生成时间: 2025-10-01 21:56:53
import quart
from gtts import gTTS
import os
from flask import send_from_directory
from werkzeug.utils import secure_filename

# 设置文件存储路径
UPLOAD_FOLDER = "uploads/"

# 创建Quart应用
app = quart.Quart(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

"""
    路由处理上传文本文件并转换为语音
"""
@app.route("/convert", methods=["POST"])
async def convert_text_to_speech():
    # 检查是否有文件在请求中
    if "file" not in quart.request.files:
        return {"error": "No file part"}, 400

    file = quart.request.files["file"]
    if file.filename == "":
        return {"error": "No selected file"}, 400

    if file:
        # 确保文件名是安全的
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        try:
            # 将文本文件转换为语音
            tts = gTTS(file=open(filepath, "r").read(), lang='en')
            audio_filename = filename.split('.')[0] + ".mp3"
            tts.save(audio_filename)
            # 返回音频文件
            return await send_audio(audio_filename)
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            # 删除上传的文本文件
            os.remove(filepath)

    return {"error": "An error occurred"}, 500

"""
    辅助函数发送音频文件
"""
async def send_audio(filename):
    return await quart.send_from_directory(directory=UPLOAD_FOLDER, filename=filename, as_attachment=True)

# 启动服务
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

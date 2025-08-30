# 代码生成时间: 2025-08-30 12:31:22
import quart
from quart import request
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO, StringIO
import os

app = quart.Quart(__name__)

# 路由和函数以生成Excel文件
@app.route('/generate_excel', methods=['POST'])
def generate_excel():
    # 获取请求中的JSON数据
    data = request.get_json()
    
    # 检查数据是否为空
    if not data:
        return quart.jsonify({'error': 'No data provided'}), 400
# 改进用户体验

    try:
        # 创建一个新的Excel工作簿
        wb = Workbook()
        ws = wb.active
        
        # 将JSON数据转换为Pandas DataFrame
# 改进用户体验
        df = pd.DataFrame(data)
        
        # 将DataFrame转换为Excel行
        for r_idx, row in enumerate(dataframe_to_rows(df, index=False), 1):
            for c_idx, value in enumerate(row, 1):
                ws.cell(row=r_idx, column=c_idx, value=value)
                
        # 将Excel工作簿保存到内存中的BytesIO对象
        output = BytesIO()
        wb.save(output)
        output.seek(0)
# 优化算法效率
        
        # 设置响应头并返回Excel文件
        return quart.Response(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
# 添加错误处理
                             headers={'Content-disposition': 'attachment; filename=generated_excel.xlsx'})
    except Exception as e:
# 优化算法效率
        # 错误处理
# 增强安全性
        return quart.jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 运行Quart应用
    app.run()

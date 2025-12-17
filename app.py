# app.py - 正确的完整版本
from flask import Flask
import os

# 1. 创建 Flask 应用实例（这行必须有！）
app = Flask(__name__)

# 2. 添加路由
@app.route('/')
def home():
    return 'Hello, World! This app is now working on Render!'

@app.route('/health')
def health():
    return 'OK', 200

# 3. 启动应用（只有直接运行时才执行）
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

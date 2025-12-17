# 独立的app.py文件，作为Gunicorn入口点
# 这是一个备选方案，确保Render平台能找到正确的app实例

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

# 从app模块导入app实例
from app import app

if __name__ == "__main__":
    # 直接运行时的处理
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

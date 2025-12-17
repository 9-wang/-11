# app.py - 适配网站结构的版本
import os
import sys

# 将项目根目录添加到Python路径
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# 从app模块导入create_app函数
from app import create_app

# 根据环境变量选择配置，默认使用生产环境
config_name = os.environ.get('FLASK_CONFIG', 'production')

# 创建完整的应用实例，加载所有蓝图和配置
app = create_app(config_name)

if __name__ == '__main__':
    # 使用环境变量中的PORT，默认5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(config_name == 'development'))
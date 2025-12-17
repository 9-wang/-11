import os
import sys
import logging

# 配置基本日志，确保在应用初始化前就能记录日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("正在初始化app模块...")

# 将项目的根目录添加到Python的导入路径中
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
logger.info(f"添加项目根目录到Python路径: {project_root}")

# 显式导入config模块，确保能正确导入
import config as app_config
logger.info("成功导入config模块")

# 导入Flask和扩展
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_caching import Cache

logger.info("成功导入Flask和扩展")

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'

logger.info("成功初始化扩展")

# 初始化缓存
def configure_cache(app):
    cache = Cache(app, config={
        'CACHE_TYPE': app.config.get('CACHE_TYPE', 'simple'),  # 使用simple缓存类型，生产环境可改为redis或memcached
        'CACHE_DEFAULT_TIMEOUT': app.config.get('CACHE_DEFAULT_TIMEOUT', 300),  # 默认缓存5分钟
        'CACHE_THRESHOLD': 500,  # 缓存阈值
    })
    return cache

logger.info("app模块初始化完成")
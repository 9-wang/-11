import os
import sys
import logging

# 配置基本日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("正在初始化应用...")

# 将项目的根目录添加到Python的导入路径中
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
logger.info(f"添加项目根目录到Python路径: {os.path.abspath(os.path.dirname(__file__))}")

# 导入Flask和扩展
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_caching import Cache
from flask_compress import Compress

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
        'CACHE_TYPE': app.config.get('CACHE_TYPE', 'simple'),
        'CACHE_DEFAULT_TIMEOUT': app.config.get('CACHE_DEFAULT_TIMEOUT', 300),
        'CACHE_THRESHOLD': 500,
    })
    return cache

# 显式导入config模块
import config as app_config
logger.info("成功导入config模块")

# 根据环境变量选择配置，默认使用开发环境
config_name = os.environ.get('FLASK_CONFIG', 'development')
logger.info(f"使用配置名称: {config_name}")

# 创建Flask应用实例
app = Flask(__name__)
logger.info("成功创建Flask应用实例")

# 加载配置
app.config.from_object(app_config.config[config_name])
logger.info("成功加载配置")

# 配置JSON响应，确保中文显示正常
app.config['JSON_AS_ASCII'] = False

# 配置CORS，允许所有来源访问
CORS(app)
logger.info("成功配置CORS")

# 性能优化配置
# 启用gzip压缩
app.config['COMPRESS_REGISTER'] = True

# 静态文件缓存设置
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 3600  # 1小时

# 模板缓存设置
app.config['TEMPLATES_AUTO_RELOAD'] = app.config['DEBUG']  # 开发环境禁用模板缓存，生产环境启用

# 配置响应头，优化浏览器缓存和JSON编码
@app.after_request
def add_cache_headers(response):
    # 添加安全响应头
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # 静态资源缓存设置
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    # 确保JSON响应使用UTF-8编码
    if response.mimetype == 'application/json':
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

# 压缩静态文件
compress = Compress()
compress.init_app(app)
logger.info("成功配置静态文件压缩")

# 初始化扩展
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
logger.info("成功初始化扩展")

# 初始化缓存
cache = configure_cache(app)
app.cache = cache
logger.info("成功初始化缓存")

# 配置日志记录
logger.info("正在配置文件日志")
from logging.handlers import RotatingFileHandler

# 确保日志目录存在
logs_dir = os.path.join(app.root_path, 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# 配置文件日志
file_handler = RotatingFileHandler(os.path.join(logs_dir, 'app.log'), maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# 设置日志级别
app.logger.setLevel(logging.INFO)
app.logger.info('应用启动')
logger.info("成功配置文件日志")

# 配置错误处理
@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(f'404错误 - {request.path}')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f'500错误 - {e}')
    return render_template('500.html'), 500
logger.info("成功配置错误处理")

# 注册蓝图
logger.info("正在注册蓝图")

# 在所有扩展初始化后导入模型，避免循环导入
with app.app_context():
    from app.user import models as user_models
    from app.culture import models as culture_models
    from app.community import models as community_models
    from app.vr import models as vr_models
logger.info("成功导入模型")

from app.home import bp as home_bp
app.register_blueprint(home_bp)
logger.info("成功注册home蓝图")

from app.culture import bp as culture_bp
app.register_blueprint(culture_bp)
logger.info("成功注册culture蓝图")

from app.vr import bp as vr_bp
app.register_blueprint(vr_bp)
logger.info("成功注册vr蓝图")

from app.community import bp as community_bp
app.register_blueprint(community_bp)
logger.info("成功注册community蓝图")

from app.dashboard import bp as dashboard_bp
app.register_blueprint(dashboard_bp)
logger.info("成功注册dashboard蓝图")

from app.user import bp as user_bp
app.register_blueprint(user_bp)
logger.info("成功注册user蓝图")

# 注册扣子智能体蓝图
from app.ai import bp as ai_bp
app.register_blueprint(ai_bp, url_prefix='/api/ai')
logger.info("成功注册ai蓝图")

logger.info("应用实例创建成功")
logger.info(f"最终app实例类型: {type(app)}")
logger.info("应用初始化完成")

if __name__ == '__main__':
    # 使用环境变量中的PORT，默认8000
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=(config_name == 'development'))
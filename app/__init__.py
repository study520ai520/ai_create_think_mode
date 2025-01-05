from flask import Flask, render_template
from flask_login import LoginManager
from app.config.config import Config
from app.models.user import User
from app.config.mongodb import mongodb
import logging
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(user_id)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 确保MongoDB连接
    if not mongodb.ensure_connected():
        logger.error("无法连接到MongoDB，应用可能无法正常工作")
    
    # 初始化扩展
    login_manager.init_app(app)
    
    # 注册蓝图
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.analysis import bp as analysis_bp
    
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(analysis_bp)
    
    # 注册错误处理
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
        
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
        
    # 注册数据库连接错误处理
    @app.errorhandler(ConnectionError)
    def handle_db_connection_error(error):
        logger.error(f"数据库连接错误: {str(error)}")
        return render_template('500.html'), 500
        
    return app 
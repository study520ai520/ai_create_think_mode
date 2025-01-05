from flask import Flask, render_template
from flask_login import LoginManager
from app.config.config import Config
from app.models.user import User
from app.config.mongodb import mongodb

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
        
    return app 
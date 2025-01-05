from flask import Flask
from flask_login import LoginManager
from config.config import Config
from config.mongodb import mongodb

# 初始化Flask应用
app = Flask(__name__)
app.config.from_object(Config)

# 初始化LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# 连接MongoDB
mongodb.connect()

# 注册蓝图
from app.routes import main, auth, analysis
app.register_blueprint(main.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(analysis.bp)

# 关闭时清理
@app.teardown_appcontext
def shutdown_session(exception=None):
    mongodb.close() 
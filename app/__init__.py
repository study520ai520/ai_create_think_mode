from flask import Flask
from app.config.config import Config
from app.config.mongodb import mongodb
import logging

def create_app():
    """创建Flask应用实例"""
    # 创建Flask应用
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(Config)
    
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 检查MongoDB连接
    if not mongodb.connected:
        logging.error("无法连接到MongoDB，应用可能无法正常工作")
    
    # 注册蓝图
    from app.routes.main import main
    from app.routes.analysis import analysis
    
    app.register_blueprint(main)
    app.register_blueprint(analysis, url_prefix='/analysis')
    
    return app 
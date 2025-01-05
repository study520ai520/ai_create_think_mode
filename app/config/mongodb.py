from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from app.config.config import Config
import logging

class MongoDB:
    def __init__(self):
        """初始化MongoDB实例"""
        self.client = None
        self.db = None
        self.connected = False
        self.connect()
        
    def connect(self):
        """连接到MongoDB数据库"""
        try:
            # 创建客户端连接
            self.client = MongoClient(
                Config.MONGO_URI,
                serverSelectionTimeoutMS=5000  # 5秒超时
            )
            
            # 测试连接
            self.client.admin.command('ping')
            
            # 获取数据库实例
            self.db = self.client[Config.MONGO_DB]
            
            # 尝试创建索引
            self._create_indexes()
            
            self.connected = True
            logging.info("MongoDB连接成功")
            return True
            
        except ConnectionFailure as e:
            logging.error(f"MongoDB连接失败: {str(e)}")
            self.connected = False
            return False
            
        except OperationFailure as e:
            logging.error(f"MongoDB操作失败: {str(e)}")
            self.connected = False
            return False
            
        except Exception as e:
            logging.error(f"MongoDB未知错误: {str(e)}")
            self.connected = False
            return False
            
    def ensure_connected(self):
        """确保数据库已连接"""
        if not self.connected:
            return self.connect()
        try:
            # 测试连接是否有效
            self.client.admin.command('ping')
            return True
        except Exception:
            return self.connect()
            
    def _create_indexes(self):
        """创建必要的索引"""
        try:
            # 用户集合索引
            if 'users' in self.db.list_collection_names():
                self.db.users.create_index('email', unique=True)
                self.db.users.create_index('username')
            
            # 分析历史索引
            if 'analysis_history' in self.db.list_collection_names():
                self.db.analysis_history.create_index([('user_id', 1), ('created_at', -1)])
                self.db.analysis_history.create_index('model_used.model_id')
            
            # 思维模型索引
            if 'thinking_models' in self.db.list_collection_names():
                self.db.thinking_models.create_index('category')
                self.db.thinking_models.create_index('name')
                
        except Exception as e:
            logging.error(f"创建索引失败: {str(e)}")
            
    def close(self):
        """关闭数据库连接"""
        if self.client:
            try:
                self.client.close()
                self.connected = False
                logging.info("MongoDB连接已关闭")
            except Exception as e:
                logging.error(f"关闭MongoDB连接失败: {str(e)}")
                
    @property
    def users(self):
        """用户集合"""
        if not self.ensure_connected() or not self.db:
            raise ConnectionError("MongoDB未连接")
        return self.db.users
        
    @property
    def analysis_history(self):
        """分析历史集合"""
        if not self.ensure_connected() or not self.db:
            raise ConnectionError("MongoDB未连接")
        return self.db.analysis_history
        
    @property
    def thinking_models(self):
        """思维模型集合"""
        if not self.ensure_connected() or not self.db:
            raise ConnectionError("MongoDB未连接")
        return self.db.thinking_models
        
    def __del__(self):
        """析构函数，确保连接被关闭"""
        self.close()

# 创建全局MongoDB实例
mongodb = MongoDB() 
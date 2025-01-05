from pymongo import MongoClient
from app.config.config import Config

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self):
        """连接到MongoDB数据库"""
        try:
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client.get_database()
            # 创建索引
            self._create_indexes()
            return True
        except Exception as e:
            print(f"MongoDB连接错误: {str(e)}")
            return False
            
    def _create_indexes(self):
        """创建必要的索引"""
        # 用户集合索引
        self.users.create_index('email', unique=True)
        self.users.create_index('username')
        
        # 分析历史索引
        self.analysis_history.create_index([('user_id', 1), ('created_at', -1)])
        self.analysis_history.create_index('model_used.model_id')
        
        # 思维模型索引
        self.thinking_models.create_index('category')
        self.thinking_models.create_index('name')
            
    def close(self):
        """关闭数据库连接"""
        if self.client:
            self.client.close()
            
    @property
    def users(self):
        """用户集合"""
        return self.db.users
        
    @property
    def analysis_history(self):
        """分析历史集合"""
        return self.db.analysis_history
        
    @property
    def thinking_models(self):
        """思维模型集合"""
        return self.db.thinking_models
        
# 创建全局MongoDB实例
mongodb = MongoDB() 
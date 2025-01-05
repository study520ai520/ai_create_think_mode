from pymongo import MongoClient, version as pymongo_version
from pymongo.errors import ConnectionFailure, OperationFailure, ServerSelectionTimeoutError
from app.config.config import Config
import logging
import time
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

class MongoDB:
    MAX_RETRIES = 3  # 最大重试次数
    RETRY_DELAY = 2  # 重试延迟（秒）
    
    def __init__(self):
        """初始化MongoDB实例"""
        self.client = None
        self.db = None
        self.connected = False
        
        # 检查pymongo版本
        logger.info(f"PyMongo版本: {pymongo_version}")
        
        # 解析MongoDB URI
        self._parse_uri()
        
        # 尝试连接
        self.connect()
    
    def _parse_uri(self):
        """解析并验证MongoDB URI"""
        try:
            # 使用简单的无认证连接
            self.uri = f"mongodb://{Config.MONGO_HOST}:{Config.MONGO_PORT}/{Config.MONGO_DB}"
            logger.info(f"MongoDB URI: {self.uri}")
            
        except Exception as e:
            logger.error(f"URI解析错误: {str(e)}")
            raise
        
    def connect(self):
        """连接到MongoDB数据库，包含重试机制"""
        retry_count = 0
        last_error = None
        
        while retry_count < self.MAX_RETRIES:
            try:
                if retry_count > 0:
                    logger.info(f"第 {retry_count} 次重试连接MongoDB...")
                    time.sleep(self.RETRY_DELAY)
                
                # 创建客户端连接
                self.client = MongoClient(
                    self.uri,
                    serverSelectionTimeoutMS=5000,  # 5秒超时
                    connectTimeoutMS=5000,
                    socketTimeoutMS=5000,
                    maxPoolSize=50
                )
                
                # 测试连接
                self.client.admin.command('ping')
                
                # 获取数据库实例
                self.db = self.client[Config.MONGO_DB]
                
                # 验证连接
                self.db.list_collection_names()
                
                # 创建索引
                self._create_indexes()
                
                self.connected = True
                logger.info("MongoDB连接成功")
                return True
                
            except ServerSelectionTimeoutError as e:
                last_error = f"MongoDB服务器选择超时: {str(e)}"
                logger.error(last_error)
                
            except ConnectionFailure as e:
                last_error = f"MongoDB连接失败: {str(e)}"
                logger.error(last_error)
                
            except Exception as e:
                last_error = f"MongoDB未知错误: {str(e)}, 类型: {type(e)}"
                logger.error(last_error)
            
            retry_count += 1
            self.connected = False
            
        # 所有重试都失败了
        if last_error:
            logger.error(f"MongoDB连接失败，已重试 {retry_count} 次。最后的错误: {last_error}")
        return False
            
    def ensure_connected(self):
        """确保数据库已连接"""
        if not self.connected or self.db is None:
            return self.connect()
            
        try:
            # 测试连接是否有效
            self.client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"MongoDB连接检查失败: {str(e)}")
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
            logger.error(f"创建索引失败: {str(e)}")
            
    def close(self):
        """关闭数据库连接"""
        if self.client:
            try:
                self.client.close()
                self.connected = False
                logger.info("MongoDB连接已关闭")
            except Exception as e:
                logger.error(f"关闭MongoDB连接失败: {str(e)}")
                
    @property
    def users(self):
        """用户集合"""
        if not self.ensure_connected() or self.db is None:
            raise ConnectionError("MongoDB未连接")
        return self.db.users
        
    @property
    def analysis_history(self):
        """分析历史集合"""
        if not self.ensure_connected() or self.db is None:
            raise ConnectionError("MongoDB未连接")
        return self.db.analysis_history
        
    @property
    def thinking_models(self):
        """思维模型集合"""
        if not self.ensure_connected() or self.db is None:
            raise ConnectionError("MongoDB未连接")
        return self.db.thinking_models
        
    def __del__(self):
        """析构函数，确保连接被关闭"""
        self.close()

# 创建全局MongoDB实例
mongodb = MongoDB() 
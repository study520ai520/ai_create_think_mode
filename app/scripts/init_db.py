from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from app.config.config import Config
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def init_db():
    """初始化数据库"""
    try:
        # 创建客户端连接
        client = MongoClient(
            Config.MONGO_URI,
            serverSelectionTimeoutMS=5000  # 5秒超时
        )
        
        # 测试连接
        client.admin.command('ping')
        logger.info("MongoDB连接成功")
        
        # 获取数据库实例
        db = client[Config.MONGO_DB]
        
        # 创建集合
        collections = ['thinking_models', 'users', 'analysis_history']
        existing_collections = db.list_collection_names()
        
        for collection in collections:
            if collection not in existing_collections:
                db.create_collection(collection)
                logger.info(f"创建集合: {collection}")
        
        # 插入初始思维模型数据
        models = [
            {
                'name': 'SWOT分析',
                'description': '用于分析项目或商业企业的优势、劣势、机会和威胁',
                'category': 'decision',
                'steps': [
                    '分析内部优势(Strengths)',
                    '分析内部劣势(Weaknesses)',
                    '分析外部机会(Opportunities)',
                    '分析外部威胁(Threats)'
                ],
                'key_features': [
                    '全面性分析',
                    '内外部结合',
                    '战略决策',
                    '风险评估'
                ],
                'application_scenarios': [
                    '项目可行性分析',
                    '企业战略规划',
                    '产品发展评估',
                    '竞争策略制定'
                ],
                'example': '例如：分析一个新产品上市的可行性'
            },
            {
                'name': '5W1H分析',
                'description': '通过提问What、Why、Where、When、Who、How来全面分析问题',
                'category': 'problem_solving',
                'steps': [
                    '明确是什么问题(What)',
                    '为什么会发生(Why)',
                    '问题发生在哪里(Where)',
                    '问题什么时候发生(When)',
                    '谁与问题相关(Who)',
                    '如何解决问题(How)'
                ],
                'key_features': [
                    '系统性思考',
                    '全面性分析',
                    '问题定位',
                    '解决方案'
                ],
                'application_scenarios': [
                    '问题分析',
                    '事件调查',
                    '流程优化',
                    '项目规划'
                ],
                'example': '例如：分析一个客户投诉事件'
            }
        ]
        
        # 如果集合为空，则插入数据
        if db.thinking_models.count_documents({}) == 0:
            result = db.thinking_models.insert_many(models)
            logger.info(f"插入思维模型数据: {len(result.inserted_ids)}条")
        
        # 创建索引
        db.users.create_index('email', unique=True)
        db.users.create_index('username')
        db.analysis_history.create_index([('user_id', 1), ('created_at', -1)])
        db.analysis_history.create_index('model_used.model_id')
        db.thinking_models.create_index('category')
        db.thinking_models.create_index('name')
        logger.info("创建索引完成")
        
        logger.info("数据库初始化完成")
        return True
        
    except ConnectionFailure as e:
        logger.error(f"MongoDB连接失败: {str(e)}")
        return False
        
    except OperationFailure as e:
        logger.error(f"MongoDB操作失败: {str(e)}")
        return False
        
    except Exception as e:
        logger.error(f"初始化数据库时出错: {str(e)}")
        return False
        
    finally:
        if 'client' in locals():
            client.close()

if __name__ == '__main__':
    init_db() 
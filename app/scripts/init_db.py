from pymongo import MongoClient
from app.config.config import Config

def init_db():
    """初始化数据库"""
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.MONGO_DB]
    
    # 创建集合
    if 'thinking_models' not in db.list_collection_names():
        db.create_collection('thinking_models')
    if 'users' not in db.list_collection_names():
        db.create_collection('users')
    if 'analysis_history' not in db.list_collection_names():
        db.create_collection('analysis_history')
    
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
            'example': '例如：分析一个客户投诉事件'
        }
    ]
    
    # 如果集合为空，则插入数据
    if db.thinking_models.count_documents({}) == 0:
        db.thinking_models.insert_many(models)
    
    print('数据库初始化完成')

if __name__ == '__main__':
    init_db() 
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
import logging

# 配置日志格式
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
logger.info("开始加载环境变量...")
load_dotenv()
logger.info(f"环境变量文件路径: {os.path.abspath('.env')}")

class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # MongoDB配置
    MONGO_USERNAME = os.getenv('MONGO_USERNAME', '')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', '')
    MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
    MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
    MONGO_DB = os.getenv('MONGO_DB', 'think_mode_db')
    MONGO_AUTH_SOURCE = os.getenv('MONGO_AUTH_SOURCE', 'admin')
    
    # 记录MongoDB配置信息（密码除外）
    logger.info(f"MongoDB配置信息:")
    logger.info(f"- 用户名: {MONGO_USERNAME}")
    logger.info(f"- 主机: {MONGO_HOST}")
    logger.info(f"- 端口: {MONGO_PORT}")
    logger.info(f"- 数据库: {MONGO_DB}")
    logger.info(f"- 认证源: {MONGO_AUTH_SOURCE}")
    
    # 优先使用完整的MongoDB URI（如果提供）
    MONGO_URI = os.getenv('MONGODB_URI')
    logger.info(f"是否提供了完整的MONGODB_URI: {'是' if MONGO_URI else '否'}")
    
    # 如果没有提供完整URI，则构建URI
    if not MONGO_URI:
        if MONGO_USERNAME and MONGO_PASSWORD:
            MONGO_URI = f"mongodb://{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource={MONGO_AUTH_SOURCE}"
            logger.info("使用用户名密码构建MongoDB URI")
        else:
            MONGO_URI = f"mongodb://localhost:27017/{MONGO_DB}"
            logger.info("使用本地默认MongoDB URI")
    
    # 记录最终的URI（隐藏密码）
    if MONGO_PASSWORD:
        safe_uri = MONGO_URI.replace(quote_plus(MONGO_PASSWORD), '****')
    else:
        safe_uri = MONGO_URI
    logger.info(f"最终MongoDB URI: {safe_uri}")
    
    # 如果没有用户名密码，尝试直接连接本地MongoDB
    if not (MONGO_USERNAME and MONGO_PASSWORD) and MONGO_HOST == 'localhost':
        MONGO_URI = f"mongodb://localhost:27017/{MONGO_DB}"
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    
    # 思维模型配置
    THINKING_MODELS = {
        'decision': {
            'SWOT': {
                'name': 'SWOT分析',
                'description': '分析优势、劣势、机会和威胁',
                'steps': ['识别内部优势', '评估内部劣势', '发现外部机会', '预测潜在威胁', '制定应对策略']
            },
            'DecisionTree': {
                'name': '决策树分析',
                'description': '通过树状结构展示决策过程和结果',
                'steps': ['定义决策问题', '识别可能选项', '评估各项结果', '计算概率和收益', '选择最优路径']
            }
        },
        'problem_solving': {
            '5W1H': {
                'name': '5W1H分析',
                'description': '从六个维度全面分析问题',
                'steps': ['What-确定问题', 'Why-分析原因', 'When-时间节点', 'Where-发生地点', 'Who-相关人员', 'How-解决方法']
            },
            'RootCause': {
                'name': '根本原因分析',
                'description': '通过持续追问找出问题根源',
                'steps': ['定义问题', '收集数据', '识别可能原因', '确定根本原因', '制定解决方案']
            }
        },
        'innovation': {
            'SixHats': {
                'name': '六顶思考帽',
                'description': '从不同角度思考问题',
                'steps': ['白帽-事实', '红帽-情感', '黑帽-批判', '黄帽-积极', '绿帽-创新', '蓝帽-管理']
            }
        },
        'system': {
            'SystemDynamics': {
                'name': '系统动力学',
                'description': '分析系统要素间的相互作用',
                'steps': ['系统边界定义', '要素识别', '关系分析', '反馈环路识别', '动态模拟']
            }
        }
    }
    
    # 应用配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'} 
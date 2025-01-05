from datetime import datetime
from bson import ObjectId
from app.config.mongodb import mongodb

class Analysis:
    def __init__(self, user_id, question, model_used, analysis_result=None,
                 visualization=None, _id=None):
        self.user_id = user_id
        self.question = question
        self.model_used = model_used  # 包含model_id, name, category
        self.analysis_result = analysis_result or {
            'summary': '',
            'details': {},
            'recommendations': []
        }
        self.visualization = visualization or {
            'type': '',
            'data': {},
            'mermaid_code': ''
        }
        self.id = str(_id) if _id else None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.feedback = {
            'rating': None,
            'comments': '',
            'helpful': None
        }
        
    def to_dict(self):
        """转换为字典格式"""
        return {
            'user_id': ObjectId(self.user_id),
            'question': self.question,
            'model_used': self.model_used,
            'analysis_result': self.analysis_result,
            'visualization': self.visualization,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'feedback': self.feedback
        }
        
    @classmethod
    def from_dict(cls, data):
        """从字典创建实例"""
        analysis = cls(
            user_id=str(data['user_id']),
            question=data['question'],
            model_used=data['model_used'],
            analysis_result=data.get('analysis_result', {
                'summary': '',
                'details': {},
                'recommendations': []
            }),
            visualization=data.get('visualization', {
                'type': '',
                'data': {},
                'mermaid_code': ''
            }),
            _id=data.get('_id')
        )
        analysis.created_at = data.get('created_at', datetime.utcnow())
        analysis.updated_at = data.get('updated_at', datetime.utcnow())
        analysis.feedback = data.get('feedback', {
            'rating': None,
            'comments': '',
            'helpful': None
        })
        return analysis
        
    def save(self):
        """保存到数据库"""
        self.updated_at = datetime.utcnow()
        data = self.to_dict()
        if self.id:
            mongodb.analysis_history.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': data}
            )
        else:
            result = mongodb.analysis_history.insert_one(data)
            self.id = str(result.inserted_id)
        return self.id
        
    @classmethod
    def find_by_id(cls, analysis_id):
        """根据ID查找分析记录"""
        data = mongodb.analysis_history.find_one({'_id': ObjectId(analysis_id)})
        return cls.from_dict(data) if data else None
        
    @classmethod
    def find_by_user(cls, user_id, limit=10, skip=0):
        """查找用户的分析历史"""
        cursor = mongodb.analysis_history.find(
            {'user_id': ObjectId(user_id)}
        ).sort('created_at', -1).skip(skip).limit(limit)
        return [cls.from_dict(data) for data in cursor]
        
    def update_result(self, analysis_result, visualization=None):
        """更新分析结果"""
        self.analysis_result = analysis_result
        if visualization:
            self.visualization = visualization
        self.save()
        
    def add_feedback(self, rating, comments='', helpful=None):
        """添加用户反馈"""
        self.feedback = {
            'rating': rating,
            'comments': comments,
            'helpful': helpful
        }
        self.save()
        
    def get_visualization(self):
        """获取可视化数据"""
        return self.visualization
        
    @classmethod
    def get_model_usage_stats(cls, model_id):
        """获取模型使用统计"""
        pipeline = [
            {'$match': {'model_used.model_id': str(model_id)}},
            {'$group': {
                '_id': None,
                'total_uses': {'$sum': 1},
                'avg_rating': {'$avg': '$feedback.rating'},
                'helpful_count': {
                    '$sum': {'$cond': ['$feedback.helpful', 1, 0]}
                }
            }}
        ]
        result = list(mongodb.analysis_history.aggregate(pipeline))
        return result[0] if result else None 
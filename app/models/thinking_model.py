from datetime import datetime
from bson import ObjectId
from app.config.mongodb import mongodb

class ThinkingModel:
    def __init__(self, name, category, description, steps=None, key_features=None,
                 application_scenarios=None, examples=None, _id=None):
        self.name = name
        self.category = category
        self.description = description
        self.steps = steps or []
        self.key_features = key_features or []
        self.application_scenarios = application_scenarios or []
        self.examples = examples or []
        self.id = str(_id) if _id else None
        self.visualization_template = {
            'type': 'default',
            'structure': {}
        }
        self.effectiveness_stats = {
            'usage_count': 0,
            'average_rating': 0.0,
            'success_rate': 0.0,
            'total_ratings': 0,
            'total_success': 0
        }
        
    def to_dict(self):
        """转换为字典格式"""
        return {
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'steps': self.steps,
            'key_features': self.key_features,
            'application_scenarios': self.application_scenarios,
            'examples': self.examples,
            'visualization_template': self.visualization_template,
            'effectiveness_stats': self.effectiveness_stats
        }
        
    @classmethod
    def from_dict(cls, data):
        """从字典创建实例"""
        model = cls(
            name=data['name'],
            category=data['category'],
            description=data['description'],
            steps=data.get('steps', []),
            key_features=data.get('key_features', []),
            application_scenarios=data.get('application_scenarios', []),
            examples=data.get('examples', []),
            _id=data.get('_id')
        )
        model.visualization_template = data.get('visualization_template', {
            'type': 'default',
            'structure': {}
        })
        model.effectiveness_stats = data.get('effectiveness_stats', {
            'usage_count': 0,
            'average_rating': 0.0,
            'success_rate': 0.0,
            'total_ratings': 0,
            'total_success': 0
        })
        return model
        
    def save(self):
        """保存到数据库"""
        data = self.to_dict()
        if self.id:
            mongodb.thinking_models.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': data}
            )
        else:
            result = mongodb.thinking_models.insert_one(data)
            self.id = str(result.inserted_id)
        return self.id
        
    @classmethod
    def find_by_id(cls, model_id):
        """根据ID查找模型"""
        data = mongodb.thinking_models.find_one({'_id': ObjectId(model_id)})
        return cls.from_dict(data) if data else None
        
    @classmethod
    def find_by_category(cls, category):
        """根据类别查找模型"""
        cursor = mongodb.thinking_models.find({'category': category})
        return [cls.from_dict(data) for data in cursor]
        
    @classmethod
    def find_all(cls):
        """获取所有模型"""
        cursor = mongodb.thinking_models.find()
        return [cls.from_dict(data) for data in cursor]
        
    def update_stats(self, rating, success=True):
        """更新模型效果统计"""
        self.effectiveness_stats['usage_count'] += 1
        if rating:
            total = self.effectiveness_stats['average_rating'] * \
                   self.effectiveness_stats['total_ratings']
            self.effectiveness_stats['total_ratings'] += 1
            self.effectiveness_stats['average_rating'] = \
                (total + rating) / self.effectiveness_stats['total_ratings']
                
        if success:
            self.effectiveness_stats['total_success'] += 1
            
        self.effectiveness_stats['success_rate'] = \
            self.effectiveness_stats['total_success'] / \
            self.effectiveness_stats['usage_count']
            
        self.save()
        
    def get_visualization_template(self):
        """获取可视化模板"""
        return self.visualization_template
        
    def set_visualization_template(self, template_type, structure):
        """设置可视化模板"""
        self.visualization_template = {
            'type': template_type,
            'structure': structure
        }
        self.save() 
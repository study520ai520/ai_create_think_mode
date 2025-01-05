from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.config.mongodb import mongodb
from bson import ObjectId

class User(UserMixin):
    def __init__(self, username, email, password=None, _id=None):
        self.username = username
        self.email = email
        self._password = None
        self.id = str(_id) if _id else None
        self.created_at = datetime.utcnow()
        self.preferences = {}
        self.statistics = {
            'total_analysis': 0,
            'favorite_model': None,
            'usage_frequency': {}
        }
        if password:
            self.set_password(password)
            
    def set_password(self, password):
        """设置密码"""
        self._password = generate_password_hash(password)
        
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self._password, password)
        
    def to_dict(self):
        """转换为字典格式"""
        return {
            'username': self.username,
            'email': self.email,
            'password': self._password,
            'created_at': self.created_at,
            'preferences': self.preferences,
            'statistics': self.statistics
        }
        
    @classmethod
    def from_dict(cls, data):
        """从字典创建实例"""
        user = cls(
            username=data['username'],
            email=data['email'],
            _id=data.get('_id')
        )
        user._password = data.get('password')
        user.created_at = data.get('created_at', datetime.utcnow())
        user.preferences = data.get('preferences', {})
        user.statistics = data.get('statistics', {
            'total_analysis': 0,
            'favorite_model': None,
            'usage_frequency': {}
        })
        return user
        
    def save(self):
        """保存到数据库"""
        data = self.to_dict()
        if self.id:
            mongodb.users.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': data}
            )
        else:
            result = mongodb.users.insert_one(data)
            self.id = str(result.inserted_id)
        return self.id
        
    @classmethod
    def find_by_id(cls, user_id):
        """根据ID查找用户"""
        data = mongodb.users.find_one({'_id': ObjectId(user_id)})
        return cls.from_dict(data) if data else None
        
    @classmethod
    def find_by_email(cls, email):
        """根据邮箱查找用户"""
        data = mongodb.users.find_one({'email': email})
        return cls.from_dict(data) if data else None
        
    @classmethod
    def find_by_username(cls, username):
        """根据用户名查找用户"""
        data = mongodb.users.find_one({'username': username})
        return cls.from_dict(data) if data else None
        
    def update_statistics(self, model_name):
        """更新使用统计"""
        self.statistics['total_analysis'] += 1
        self.statistics['usage_frequency'][model_name] = \
            self.statistics['usage_frequency'].get(model_name, 0) + 1
            
        # 更新最常用模型
        max_usage = 0
        for model, count in self.statistics['usage_frequency'].items():
            if count > max_usage:
                max_usage = count
                self.statistics['favorite_model'] = model
                
        self.save()
        
    def get_favorite_models(self, limit=3):
        """获取用户最常用的模型"""
        usage = self.statistics['usage_frequency']
        return sorted(usage.items(), key=lambda x: x[1], reverse=True)[:limit] 
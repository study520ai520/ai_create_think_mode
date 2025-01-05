import openai
from app.config.config import Config
from app.models.thinking_model import ThinkingModel
from app.services.ai_engine import ai_engine

class ModelMatcher:
    def __init__(self):
        self.models = {}
        self.load_models()
        openai.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        
    def load_models(self):
        """加载所有思维模型"""
        models = ThinkingModel.find_all()
        for model in models:
            self.models[model.id] = model
            
    def refresh_models(self):
        """刷新模型列表"""
        self.models.clear()
        self.load_models()
        
    def match_model(self, question):
        """匹配最适合的思维模型"""
        try:
            # 分析问题特征
            analysis = ai_engine.analyze_question(question)
            if not analysis:
                return None
                
            # 构建匹配提示
            prompt = self._build_matching_prompt(question, analysis)
            
            # 调用OpenAI进行匹配
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个思维模型专家，擅长为不同类型的问题匹配最合适的思维模型。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # 解析匹配结果
            matches = self._parse_matching_result(response.choices[0].message['content'])
            
            # 返回最佳匹配的模型及匹配原因
            return self._get_best_match(matches)
        except Exception as e:
            print(f"模型匹配时出错: {str(e)}")
            return None
            
    def get_model_by_id(self, model_id):
        """根据ID获取模型"""
        return self.models.get(model_id)
        
    def get_models_by_category(self, category):
        """获取指定类别的所有模型"""
        return [model for model in self.models.values() if model.category == category]
        
    def get_all_models(self):
        """获取所有模型"""
        return list(self.models.values())
        
    def _build_matching_prompt(self, question, analysis):
        """构建匹配提示信息"""
        models_info = self._get_models_info()
        return f"""请分析以下问题和特征，从给定的思维模型中选择最合适的3个模型：

问题：{question}

问题分析：
关键词：{', '.join(analysis['keywords'])}
特征：{chr(10).join(analysis['features'])}
上下文：{analysis['context']}

可选思维模型：
{models_info}

请按照以下格式输出匹配结果：
1. 模型名称：[匹配度分数]
   匹配原因：...
2. 模型名称：[匹配度分数]
   匹配原因：...
3. 模型名称：[匹配度分数]
   匹配原因：...

注意：
1. 匹配度分数范围为0-100
2. 请详细说明每个模型的匹配原因
3. 按匹配度从高到低排序"""
            
    def _get_models_info(self):
        """获取所有模型信息"""
        info = []
        for model in self.models.values():
            info.append(f"""
{model.name}（{model.category}类）
描述：{model.description}
适用场景：{', '.join(model.application_scenarios)}
关键特征：{', '.join(model.key_features)}""")
        return '\n'.join(info)
        
    def _parse_matching_result(self, text):
        """解析匹配结果"""
        matches = []
        current_match = {}
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line[0].isdigit() and '：' in line:
                if current_match:
                    matches.append(current_match)
                current_match = {}
                # 解析模型名称和匹配度
                name_score = line.split('：')[1].strip()
                name = name_score[:name_score.rfind('[')].strip()
                score = int(name_score[name_score.rfind('[')+1:name_score.rfind(']')])
                current_match['name'] = name
                current_match['score'] = score
            elif line.startswith('匹配原因：'):
                current_match['reason'] = line[5:].strip()
                
        if current_match:
            matches.append(current_match)
            
        return matches
        
    def _get_best_match(self, matches):
        """获取最佳匹配的模型"""
        if not matches:
            return None
            
        # 找到匹配度最高的模型
        best_match = max(matches, key=lambda x: x['score'])
        
        # 查找对应的模型实例
        for model in self.models.values():
            if model.name == best_match['name']:
                return {
                    'model': model,
                    'score': best_match['score'],
                    'reason': best_match['reason']
                }
                
        return None

# 创建全局模型匹配器实例
model_matcher = ModelMatcher() 
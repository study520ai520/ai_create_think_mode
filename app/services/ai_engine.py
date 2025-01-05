import openai
from app.config.config import Config
from app.models.thinking_model import ThinkingModel

class AIEngine:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        
    def analyze_question(self, question):
        """分析用户问题，提取关键信息"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的问题分析专家，擅长提取问题的关键信息和特征。"},
                    {"role": "user", "content": f"请分析以下问题，提取关键信息和特征：\n{question}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return {
                'keywords': self._extract_keywords(response.choices[0].message['content']),
                'features': self._extract_features(response.choices[0].message['content']),
                'context': response.choices[0].message['content']
            }
        except Exception as e:
            print(f"分析问题时出错: {str(e)}")
            return None
            
    def generate_analysis(self, question, model: ThinkingModel):
        """使用指定思维模型生成分析结果"""
        try:
            # 构建提示信息
            prompt = self._build_analysis_prompt(question, model)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的思维模型分析专家，擅长使用各种思维模型分析问题。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )
            
            # 解析分析结果
            return self._parse_analysis_result(response.choices[0].message['content'])
        except Exception as e:
            print(f"生成分析结果时出错: {str(e)}")
            return None
            
    def generate_visualization(self, analysis_result, model: ThinkingModel):
        """生成可视化数据"""
        try:
            template = model.get_visualization_template()
            prompt = self._build_visualization_prompt(analysis_result, template)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的数据可视化专家，擅长使用Mermaid生成图表。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return {
                'type': template['type'],
                'data': self._extract_visualization_data(response.choices[0].message['content']),
                'mermaid_code': self._extract_mermaid_code(response.choices[0].message['content'])
            }
        except Exception as e:
            print(f"生成可视化数据时出错: {str(e)}")
            return None
            
    def _build_analysis_prompt(self, question, model: ThinkingModel):
        """构建分析提示信息"""
        return f"""请使用{model.name}思维模型分析以下问题：

问题：{question}

模型说明：{model.description}

分析步骤：
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(model.steps))}

请按照以下格式输出分析结果：
1. 总结：简要概述分析结果
2. 详细分析：按照模型步骤逐一分析
3. 建议：基于分析给出具体建议

注意：分析要具体、深入、可操作。"""
            
    def _build_visualization_prompt(self, analysis_result, template):
        """构建可视化提示信息"""
        return f"""请根据以下分析结果，生成一个Mermaid图表：

分析结果：
{analysis_result}

可视化类型：{template['type']}
结构要求：{template['structure']}

请生成符合Mermaid语法的图表代码，确保图表清晰展示分析结果的关键信息和关系。"""
            
    def _extract_keywords(self, text):
        """从文本中提取关键词"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个关键词提取专家。"},
                    {"role": "user", "content": f"请从以下文本中提取5-10个关键词：\n{text}"}
                ],
                temperature=0.5,
                max_tokens=100
            )
            return [kw.strip() for kw in response.choices[0].message['content'].split(',')]
        except Exception:
            return []
            
    def _extract_features(self, text):
        """从文本中提取特征"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个文本特征提取专家。"},
                    {"role": "user", "content": f"请从以下文本中提取3-5个主要特征：\n{text}"}
                ],
                temperature=0.5,
                max_tokens=100
            )
            return [f.strip() for f in response.choices[0].message['content'].split('\n')]
        except Exception:
            return []
            
    def _parse_analysis_result(self, text):
        """解析分析结果文本"""
        sections = text.split('\n\n')
        result = {
            'summary': '',
            'details': {},
            'recommendations': []
        }
        
        current_section = None
        for section in sections:
            if section.startswith('总结：'):
                result['summary'] = section[3:].strip()
            elif section.startswith('详细分析：'):
                current_section = 'details'
            elif section.startswith('建议：'):
                current_section = 'recommendations'
                result['recommendations'] = [r.strip() for r in section[3:].split('\n') if r.strip()]
            elif current_section == 'details':
                parts = section.split('：', 1)
                if len(parts) == 2:
                    result['details'][parts[0].strip()] = parts[1].strip()
                    
        return result
        
    def _extract_visualization_data(self, text):
        """从文本中提取可视化数据"""
        try:
            # 提取图表中的数据部分
            data_section = text[text.find('```mermaid')+10:text.rfind('```')]
            return self._parse_mermaid_data(data_section)
        except Exception:
            return {}
            
    def _extract_mermaid_code(self, text):
        """提取Mermaid代码"""
        try:
            start = text.find('```mermaid')
            end = text.rfind('```')
            if start != -1 and end != -1:
                return text[start+10:end].strip()
        except Exception:
            pass
        return ''
        
    def _parse_mermaid_data(self, mermaid_code):
        """解析Mermaid代码中的数据"""
        data = {
            'nodes': [],
            'relationships': []
        }
        
        lines = mermaid_code.split('\n')
        for line in lines:
            line = line.strip()
            if '-->' in line or '---' in line:
                parts = line.split('--')
                if len(parts) >= 2:
                    data['relationships'].append({
                        'from': parts[0].strip(),
                        'to': parts[-1].strip(),
                        'type': 'arrow' if '>' in line else 'line'
                    })
            elif line and not line.startswith('graph'):
                data['nodes'].append(line)
                
        return data

# 创建全局AI引擎实例
ai_engine = AIEngine() 
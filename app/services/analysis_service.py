from app.models.analysis import Analysis
from app.services.ai_engine import ai_engine
from app.services.model_matcher import model_matcher

class AnalysisService:
    def analyze_question(self, user_id, question):
        """分析问题并生成结果"""
        # 1. 匹配思维模型
        model, analysis = model_matcher.match_model(question)
        if not model:
            return None, analysis  # analysis 此时包含错误信息
            
        # 2. 使用匹配的模型生成分析
        analysis_result = ai_engine.generate_analysis(question, model.name)
        if not analysis_result:
            return None, "分析生成失败"
            
        # 3. 生成可视化
        visualization = ai_engine.generate_visualization(analysis_result)
            
        # 4. 保存分析记录
        analysis = Analysis(
            user_id=user_id,
            question=question,
            model_used=model._id,
            analysis_result=analysis_result,
            visualization=visualization
        )
        analysis_id = analysis.save()
            
        return {
            'analysis_id': analysis_id,
            'model': model.name,
            'analysis': analysis_result,
            'visualization': visualization
        }, None
            
    def get_user_analysis_history(self, user_id, limit=10):
        """获取用户的分析历史"""
        return Analysis.find_by_user(user_id, limit)
            
    def get_analysis_by_id(self, analysis_id):
        """根据ID获取分析记录"""
        return Analysis.find_by_id(analysis_id)
            
    def delete_analysis(self, analysis_id):
        """删除分析记录"""
        analysis = Analysis.find_by_id(analysis_id)
        if analysis:
            analysis.delete()
            return True
        return False
            
# 创建全局分析服务实例
analysis_service = AnalysisService() 
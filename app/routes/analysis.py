from flask import Blueprint, request, jsonify
from app.services.analysis_service import analysis_service
from datetime import datetime
from app.config.mongodb import mongodb

analysis = Blueprint('analysis', __name__)

@analysis.route('/analyze', methods=['POST'])
def analyze():
    """处理分析请求"""
    data = request.get_json()
    
    if not data or 'question' not in data or 'model_type' not in data:
        return jsonify({
            'success': False,
            'error': '请提供问题描述和思维模型类型'
        }), 400
    
    try:
        # 进行分析
        result = analysis_service.analyze_question(
            data['question'],
            data['model_type']
        )
        
        # 保存分析历史
        history_record = {
            'question': data['question'],
            'model_type': data['model_type'],
            'result': result,
            'created_at': datetime.utcnow()
        }
        mongodb.analysis_history.insert_one(history_record)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 
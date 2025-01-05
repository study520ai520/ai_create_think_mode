from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.analysis_service import analysis_service
from app.services.model_matcher import model_matcher

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@bp.route('/analyze', methods=['POST'])
@login_required
def analyze():
    """分析问题"""
    question = request.json.get('question')
    if not question:
        return jsonify({'error': '请输入问题'}), 400
        
    result, error = analysis_service.analyze_question(current_user.id, question)
    if error:
        return jsonify({'error': error}), 400
        
    return jsonify(result)
    
@bp.route('/history')
@login_required
def history():
    """查看分析历史"""
    analyses = analysis_service.get_user_analysis_history(current_user.id)
    return render_template('analysis/history.html', analyses=analyses)
    
@bp.route('/detail/<analysis_id>')
@login_required
def detail(analysis_id):
    """查看分析详情"""
    analysis = analysis_service.get_analysis_by_id(analysis_id)
    if not analysis or str(analysis.user_id) != str(current_user.id):
        return render_template('404.html'), 404
        
    return render_template('analysis/detail.html', analysis=analysis)
    
@bp.route('/models')
@login_required
def models():
    """查看思维模型列表"""
    category = request.args.get('category')
    if category:
        models = model_matcher.get_models_by_category(category)
    else:
        models = model_matcher.models.values()
    return render_template('analysis/models.html', models=models) 
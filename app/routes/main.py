from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from app.models.thinking_model import ThinkingModel
from app.forms import AnalysisForm
from app.config.config import Config

# 创建蓝图
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """首页"""
    # 创建分析表单
    form = AnalysisForm()
    
    # 获取所有思维模型，按类别分组
    models = ThinkingModel.find_all()
    thinking_models = {}
    for model in models:
        if model.category not in thinking_models:
            thinking_models[model.category] = []
        thinking_models[model.category].append(model)
    
    # 如果URL中有model_id参数，预选该模型
    model_id = request.args.get('model_id')
    if model_id:
        form.auto_match.data = False
        form.model_id.data = model_id
    
    return render_template('index.html', 
                         form=form,
                         thinking_models=thinking_models)

@main.route('/models')
def models():
    """思维模型库"""
    # 获取所有思维模型
    all_models = ThinkingModel.find_all()
    
    # 按类别分组模型
    models = {}
    categories = []
    for model in all_models:
        if model.category not in models:
            models[model.category] = []
            categories.append(model.category)
        models[model.category].append(model)
    
    # 类别名称映射
    category_names = {
        'decision': '决策分析',
        'problem_solving': '问题解决',
        'innovation': '创新思维',
        'system': '系统思维'
    }
    
    return render_template('models.html',
                         models=models,
                         categories=categories,
                         category_names=category_names)

@main.route('/terms')
def terms():
    """服务条款"""
    return render_template('terms.html')

@main.route('/privacy')
def privacy():
    """隐私政策"""
    return render_template('privacy.html') 
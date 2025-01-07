from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.forms import AnalysisForm
from app.config.mongodb import mongodb
from app.config.config import Config
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    """首页"""
    form = AnalysisForm()
    
    # 从配置中获取思维模型数据
    thinking_models = Config.THINKING_MODELS
    
    return render_template('index.html', 
                         form=form,
                         thinking_models=thinking_models)

@main.route('/models')
def models():
    """思维模型库"""
    # 从配置中获取思维模型数据
    thinking_models = Config.THINKING_MODELS
    
    # 类别名称映射
    category_names = {
        'decision': '决策分析',
        'problem_solving': '问题解决',
        'innovation': '创新思维',
        'system': '系统思维'
    }
    
    return render_template('models.html',
                         thinking_models=thinking_models,
                         category_names=category_names)

@main.route('/history')
def history():
    """分析历史"""
    # 获取分析历史记录
    history_records = list(mongodb.analysis_history.find().sort('created_at', -1))
    return render_template('history.html', history=history_records) 
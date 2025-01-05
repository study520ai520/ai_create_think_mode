from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.forms import AnalysisForm
from app.config.mongodb import mongodb
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    """首页"""
    form = AnalysisForm()
    return render_template('index.html', form=form)

@main.route('/models')
def models():
    """思维模型库"""
    return render_template('models.html')

@main.route('/history')
def history():
    """分析历史"""
    # 获取分析历史记录
    history_records = list(mongodb.analysis_history.find().sort('created_at', -1))
    return render_template('history.html', history=history_records) 
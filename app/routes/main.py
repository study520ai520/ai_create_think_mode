from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """主页"""
    return render_template('main/index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    """用户仪表板"""
    return render_template('main/dashboard.html') 
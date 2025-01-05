from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.forms import LoginForm, RegisterForm, ProfileForm, PreferencesForm
from app.models.analysis import Analysis
from datetime import datetime, timedelta

# 创建蓝图
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('邮箱或密码错误', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        user.save()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """退出登录"""
    logout_user()
    flash('您已成功退出登录', 'info')
    return redirect(url_for('main.index'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """个人资料"""
    form = ProfileForm(current_user.username)
    pref_form = PreferencesForm()
    
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio if hasattr(current_user, 'bio') else ''
        
        pref_form.default_model.data = current_user.preferences.get('default_model', 'auto')
        pref_form.result_display.data = current_user.preferences.get('result_display', 'detailed')
        pref_form.email_notifications.data = current_user.preferences.get('email_notifications', True)
    
    # 获取本月分析次数
    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_analysis_count = Analysis.find_by_user(
        current_user.id,
        start_date=month_start
    ).count()
    
    # 获取最近的分析记录
    recent_analyses = Analysis.find_by_user(current_user.id, limit=5)
    
    return render_template('auth/profile.html',
                         form=form,
                         pref_form=pref_form,
                         monthly_analysis_count=monthly_analysis_count,
                         recent_analyses=recent_analyses)

@auth.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    """更新个人资料"""
    form = ProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        current_user.save()
        flash('个人资料已更新', 'success')
    return redirect(url_for('auth.profile'))

@auth.route('/update_preferences', methods=['POST'])
@login_required
def update_preferences():
    """更新偏好设置"""
    form = PreferencesForm()
    if form.validate_on_submit():
        current_user.preferences = {
            'default_model': form.default_model.data,
            'result_display': form.result_display.data,
            'email_notifications': form.email_notifications.data
        }
        current_user.save()
        flash('偏好设置已更新', 'success')
    return redirect(url_for('auth.profile'))

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """忘记密码"""
    # TODO: 实现忘记密码功能
    return render_template('auth/forgot_password.html') 
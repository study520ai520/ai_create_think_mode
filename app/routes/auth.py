from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.find_by_email(email):
            flash('邮箱已被注册')
            return redirect(url_for('auth.register'))
            
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        
        flash('注册成功，请登录')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')
    
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.find_by_email(email)
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
            
        flash('邮箱或密码错误')
        
    return render_template('auth/login.html')
    
@bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    return redirect(url_for('main.index')) 
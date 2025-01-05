from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    """登录表单"""
    email = StringField('邮箱', validators=[
        DataRequired(message='请输入邮箱'),
        Email(message='请输入有效的邮箱地址')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码')
    ])
    remember = BooleanField('记住我')

class RegisterForm(FlaskForm):
    """注册表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'),
        Length(min=3, max=20, message='用户名长度必须在3-20个字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='请输入邮箱'),
        Email(message='请输入有效的邮箱地址')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码'),
        Length(min=8, message='密码长度不能少于8个字符')
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    accept_terms = BooleanField('同意服务条款', validators=[
        DataRequired(message='必须同意服务条款才能注册')
    ])

    def validate_username(self, field):
        """验证用户名是否已存在"""
        user = User.find_by_username(field.data)
        if user:
            raise ValidationError('该用户名已被使用')

    def validate_email(self, field):
        """验证邮箱是否已存在"""
        user = User.find_by_email(field.data)
        if user:
            raise ValidationError('该邮箱已被注册')

class ProfileForm(FlaskForm):
    """个人资料表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'),
        Length(min=3, max=20, message='用户名长度必须在3-20个字符之间')
    ])
    email = StringField('邮箱', render_kw={'readonly': True})
    bio = TextAreaField('个人简介', validators=[
        Length(max=200, message='个人简介不能超过200个字符')
    ])

    def __init__(self, original_username, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, field):
        """验证用户名是否已存在（排除当前用户）"""
        if field.data != self.original_username:
            user = User.find_by_username(field.data)
            if user:
                raise ValidationError('该用户名已被使用')

class PreferencesForm(FlaskForm):
    """偏好设置表单"""
    default_model = SelectField('默认思维模型', 
        choices=[('auto', '自动选择'), ('swot', 'SWOT分析'), ('5w1h', '5W1H分析')],
        validators=[DataRequired(message='请选择默认思维模型')])
    result_display = SelectField('分析结果展示方式',
        choices=[('detailed', '详细模式'), ('simple', '简洁模式')],
        validators=[DataRequired(message='请选择展示方式')])
    email_notifications = BooleanField('接收邮件通知')

class AnalysisForm(FlaskForm):
    """问题分析表单"""
    question = TextAreaField('问题描述', validators=[
        DataRequired(message='请输入问题描述'),
        Length(min=10, message='问题描述不能少于10个字符')
    ])
    auto_match = BooleanField('自动匹配模型', default=True)
    model_id = SelectField('思维模型', coerce=str)

    def __init__(self, *args, **kwargs):
        super(AnalysisForm, self).__init__(*args, **kwargs)
        from app.models.thinking_model import ThinkingModel
        # 动态加载思维模型选项
        models = ThinkingModel.find_all()
        self.model_id.choices = [(str(model.id), model.name) for model in models]

class FeedbackForm(FlaskForm):
    """反馈表单"""
    rating = SelectField('评分', choices=[(str(i), str(i)) for i in range(1, 6)],
        validators=[DataRequired(message='请选择评分')])
    comments = TextAreaField('反馈意见')
    helpful = BooleanField('这次分析对我有帮助') 
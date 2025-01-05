from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

class AnalysisForm(FlaskForm):
    """分析表单"""
    question = TextAreaField(
        '问题描述',
        validators=[
            DataRequired(message='请输入问题描述'),
            Length(min=10, max=1000, message='问题描述长度应在10-1000字之间')
        ]
    )
    model_type = SelectField(
        '思维模型',
        validators=[DataRequired(message='请选择思维模型')],
        choices=[
            ('SWOT', 'SWOT分析'),
            ('DecisionTree', '决策树分析'),
            ('5W1H', '5W1H分析'),
            ('RootCause', '根本原因分析'),
            ('SixHats', '六顶思考帽'),
            ('SystemDynamics', '系统动力学')
        ]
    ) 
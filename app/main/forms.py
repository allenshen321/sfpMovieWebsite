# main蓝图，表单

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class EditProfileForm(FlaskForm):
    """
    修改个人资料表单
    """
    username = StringField('用户名：', validators=[DataRequired(), Length(1, 64)])
    info = TextAreaField('个人简介：')
    submit = SubmitField('提交')

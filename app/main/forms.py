# main蓝图，表单

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from flask_login import current_user


class EditProfileForm(FlaskForm):
    """
    修改个人资料表单
    """
    username = StringField('用户名：', validators=[DataRequired(), Length(1, 64)])
    info = TextAreaField('个人简介：')
    submit = SubmitField('提交')


class EditPasswordForm(FlaskForm):
    """
    修改密码表单
    """
    old_pwd = StringField('旧密码:', validators=[DataRequired()])
    new_pwd = PasswordField('新密码:', validators=[DataRequired(),
                                             EqualTo('new_pwd2', message='两次密码必须一致！')])
    new_pwd2 = PasswordField('新密码：', validators=[DataRequired()])
    submit = SubmitField('确认修改')

    def validate_old_pwd(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('旧密码输入错误！')


class CommentForm(FlaskForm):
    """
    评论电影表单
    """
    body = TextAreaField('想对这个电影说点什么？', validators=[DataRequired()])
    submit = SubmitField('提交评论')

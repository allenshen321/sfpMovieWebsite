from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
    email = StringField('邮箱:', validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('记住我的登录状态！')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    email = StringField('邮箱:', validators=[DataRequired(), Email(), Length(1, 64)])
    username = StringField('用户名：',
                           validators=[DataRequired(),
                                       Length(1, 64),
                                       ])
    password = PasswordField('密码:', validators=[DataRequired(),
                                                      EqualTo('password2', message='两次密码必须一样！')
                                                      ])
    password2 = PasswordField('确认密码：', validators=[DataRequired()])
    submit = SubmitField('注册')

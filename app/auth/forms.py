from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField
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
                                       Regexp(r'^[a-zA-Z][1-9a-zA-Z._]*$', 0, '用户名必须字母开头且是字母\数字\下划线\点')])
    password = PasswordField('密码:', validators=[DataRequired(),
                                                      EqualTo('password2', message='两次密码必须一样！')
                                                      ])
    password2 = PasswordField('确认密码：', validators=[DataRequired()])
    submit = SubmitField('注册')


class AddRecommentMovieForm(FlaskForm):
    name = StringField('电影名(*):', validators=[DataRequired()])
    url = StringField('电影播放链接(*):', validators=[DataRequired()])
    cover = StringField('海报url:')
    director = StringField('导演:')
    actors = StringField('演员:')
    tags = StringField('类型(多个类型以"/"分开):')
    rating = StringField('豆瓣评分:')
    release_time = StringField('上映时间:')
    area = StringField('地区:')
    language = StringField('语言:')
    introduction = TextAreaField('剧情介绍:')
    is_recomment = BooleanField('是否是推荐电影:')
    submit = SubmitField('提交电影')


class ManageMovieForm(FlaskForm):
    is_recomment = BooleanField('推荐')
    submit = SubmitField('提交')


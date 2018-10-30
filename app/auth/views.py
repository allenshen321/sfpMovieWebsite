# 用户认证视图模块
from flask import redirect, flash, render_template, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegisterForm
from app.models import User
from app import db


'''
@auth.before_request
def before_request():
    """
    请求前确认条件
    :return:
    """
    if current_user.is_authenticated:
        current_user.ping()  # 刷新请求时间
        if not current_user.confirmed \
            and request.endpoint[:5] != 'auth' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))
'''


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """
    登录视图
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('登录成功！')
            return redirect(url_for('main.index'))
        flash('用户名或密码输入错误！！！')

    return render_template('auth/login.html', form=form)


@auth.route('/registration/', methods=['GET', 'POST'])
def registration():
    """
    注册视图
    :return:
    """
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('用户名已经被注册：')
            return redirect(url_for('auth.registration'))
        elif User.query.filter_by(email=form.email.data).first():
            flash('邮箱已经被注册了!')
            return redirect(url_for('auth.registration'))
        else:
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data
                        )
            db.session.add(user)
            db.session.commit()
            flash('注册成功！')
            return redirect(url_for('auth.login'))

    return render_template('auth/registration.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    """
    退出登录视图
    :return:
    """
    logout_user()
    flash('您已经退出登录！')
    return redirect(url_for('main.index'))



# 用户认证视图模块
from flask import redirect, flash, render_template, url_for, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegisterForm, AddRecommentMovieForm, ManageMovieForm
from app.models import User, Userlog, Movie, Tag
from app import db
from datetime import datetime
from app.decorators import admin_required
from sqlalchemy import and_


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
            # 保存用户登录日志
            userlog = Userlog(user_id=current_user.id,
                              ip=request.remote_addr,
                              log_time=datetime.now())
            db.session.add(userlog)
            db.session.commit()

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
    # 记录退出登录时的时间
    userlog = Userlog.query.filter_by(user_id=current_user.id).order_by(Userlog.log_time.desc()).first()
    userlog.logout_time = datetime.now()
    db.session.add(userlog)
    db.session.commit()
    # 退出登录
    logout_user()
    flash('您已经退出登录！')
    return redirect(url_for('main.index'))


@auth.route('/add/movie/', methods=['POST', 'GET'])
@login_required
@admin_required
def add_movie():
    """
    新增电影，已过电影已存在则更新电影信息
    :return:
    """
    form = AddRecommentMovieForm()
    if form.validate_on_submit():
        movie = Movie.query.filter_by(name=form.name.data).first()
        if movie:
            flash('电影已存在!')
            return redirect(url_for('auth.update_movie', id=movie.id))
        movie = Movie(name=form.name.data,
                      url=form.url.data,
                      cover=form.cover.data,
                      director=form.director.data,
                      actors=form.actors.data,
                      rating=form.rating.data,
                      release_time=form.release_time.data,
                      area=form.area.data,
                      language=form.language.data,
                      introduction=form.introduction.data,
                      is_recomment=form.is_recomment.data)
        tags = form.tags.data
        tag_list = tags.split('/')
        for tag_name in tag_list:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag:
                movie.tags.append(tag)
            else:
                add_tag = Tag(name=tag_name,
                              addtime=datetime.now())
                db.session.add(add_tag)
                db.session.commit()
                movie.tags.append(add_tag)
        db.session.add(movie)
        db.session.commit()
        flash('电影添加成功')
        return redirect('auth/add-recomment-movie/')
    return render_template('auth/add-movie.html', form=form)


@auth.route('/admin/update/movie/<int:id>/', methods=['POST', 'GET'])
@login_required
@admin_required
def update_movie(id):
    form = AddRecommentMovieForm()

    if form.validate_on_submit():
        movie = Movie.query.get_or_404(id)
        movie.name = form.name.data
        movie.url = form.url.data
        movie.release_time = form.release_time.data
        movie.cover = form.cover.data
        movie.director = form.director.data
        movie.actors = form.actors.data
        movie.rating = form.rating.data
        movie.area = form.area.data
        movie.language = form.language.data
        movie.introduction = form.introduction.data
        movie.is_recomment = form.is_recomment.data
        db.session.add(movie)
        db.session.commit()
        flash('电影信息已更新')
        return redirect(url_for('auth.manage_movie'))

    # 初始化form表单
    movie = Movie.query.get_or_404(id)
    if movie:
        form.name.data = movie.name
        form.url.data = movie.url
        form.release_time.data = movie.release_time
        form.cover.data = movie.cover
        form.director.data = movie.director
        form.actors.data = movie.actors
        form.rating.data = movie.rating
        form.area.data = movie.area
        form.language.data = movie.language
        form.introduction.data = movie.introduction
        form.is_recomment.data = movie.is_recomment


    return render_template('auth/update-movie.html', form=form)


@auth.route('/admin/manage/movie/')
@login_required
@admin_required
def manage_movie():
    p = {}
    p['area'] = request.args.get('area', '')
    p['time'] = request.args.get('time', '')
    p['tag'] = request.args.get('tag', '')

    # 全部电影分页
    page = request.args.get('page', 1, type=int)
    if p['tag']:
        pagination = Tag.query.filter(Tag.name == p['tag']).first().movies.filter(
            and_(Movie.area.like('%{}%'.format(p['area'])), Movie.release_time.like('%{}%'.format(p['time'])))
        ).order_by(
            Movie.rating.desc()
        ).paginate(
            page,
            per_page=current_app.config.get('FLASK_MOVIE_PER_PAGE_COUNT'),
            error_out=True
        )
    else:
        pagination = Movie.query.filter(
            and_(Movie.area.like('%{}%'.format(p['area'])), Movie.release_time.like('%{}%'.format(p['time'])))
        ).order_by(
            Movie.rating.desc()
        ).paginate(
            page,
            per_page=current_app.config.get('FLASK_MOVIE_PER_PAGE_COUNT'),
            error_out=True
        )

    # 所有标签
    tags = Tag.query.all()

    # 地区
    areas = ['中国大陆', '香港', '美国', '台湾', '韩国', '日本', '印度', '英国', '德国', '俄罗斯', '苏联', '西班牙', '法国', '巴西']

    # 电影
    movies = pagination.items

    # 年代
    times = [str(i) for i in range(2018, 1989, -1)]

    return render_template('auth/manage-index.html',
                           tags=tags,
                           areas=areas,
                           movies=movies,
                           pagination=pagination,
                           p=p,
                           times=times)


@auth.route('manage/delete/movie/<int:id>')
@login_required
@admin_required
def delete_movie(id):
    """
    删除电影视图
    :param id:
    :return:
    """
    Movie.delete(id)
    p = {}
    p['time'] = request.args.get('time', '')
    p['area'] = request.args.get('area', '')
    p['tag'] = request.args.get('tag', '')
    return redirect(url_for('auth.manage_movie', time=p['time'], area=p['area'], tag=p['tag']))


@auth.route('manage/recomment/movie/<int:id>')
@login_required
@admin_required
def recomment_movie(id):
    """
    推荐电影
    :param id:
    :return:
    """
    movie = Movie.query.get_or_404(id)
    if not movie.is_recomment:
        movie.recomment()
        flash('已成功推荐！可以在首页滚动推荐页查看了！')
    else:
        flash('您已经推荐过了，不用重复推荐！')
    time = request.args.get('time', '')
    area = request.args.get('area', '')
    tag = request.args.get('tag', '')
    print(request.url)
    print(request.environ.get('HTTP_REFERER'))
    referer = request.environ.get('HTTP_REFERER', None)
    return redirect(url_for('auth.manage_movie', time=time, area=area, tag=tag))


@auth.route('manage/unrecomment/movie/<int:id>')
@login_required
@admin_required
def unrecomment_movie(id):
    """
    取消推荐电影
    :param id:
    :return:
    """
    movie = Movie.query.filter_by(id=id).first()
    if movie.is_recommenting():
        movie.unrecomment()
        flash('已成功取消推荐！')
    else:
        flash('您还没有推荐过！')
    time = request.args.get('time', '')
    area = request.args.get('area', '')
    tag = request.args.get('tag', '')
    referer = request.environ.get('HTTP_REFERER', None)
    if referer:
        return redirect(referer)
    return redirect(url_for('auth.manage_movie', time=time, area=area, tag=tag))



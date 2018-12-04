from . import main
from app import db
from flask import render_template, request, current_app, abort, flash, url_for, redirect, session
from app.models import Movie, Tag, User, Permission, Comment, Userlog, Moviecol
from flask_login import login_required, current_user
from .forms import EditProfileForm, EditPasswordForm, CommentForm
from datetime import datetime
from sqlalchemy import and_, or_
from app.decorators import permission_required, admin_required


@main.route('/')
def index():
    """显示首页"""
    movies = {}
    tags = Tag.query.all()
    tag_dict = {}
    for tag in tags:
        # print(tag)
        tag_dict[tag.name] = tag.name
        movies[tag.name] = tag.movies.order_by(Movie.addtime.desc()).limit(15).all()
    # print(movies)

    movies['recomment_movies'] = Movie.query.filter_by(is_recomment=True).order_by(Movie.release_time.desc()).limit(5).all()

    # 按标签电影排名前10
    rank_movies = {}
    for key, value in tag_dict.items():
        rank_movies[value] = Tag.query.filter(Tag.name == value).first().movies.order_by(Movie.rating.desc()).limit(20).all()

    return render_template('main/index.html',
                           movies=movies,
                           rank_movies=rank_movies)


@main.route('/show/all/movies')
def show_all_movies():
    """显示所有电影"""
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

    return render_template('main/show-all-movies.html',
                           tags=tags,
                           areas=areas,
                           movies=movies,
                           pagination=pagination,
                           p=p,
                           times=times)


@main.route('/all/tags/')
def show_all_tags():
    """
    所有标签下的电影
    :return:
    """
    tags = Tag.query.order_by(Tag.addtime.desc()).all()
    # 全部电影分页
    page = request.args.get('page', 1, type=int)
    pagination = Movie.query.order_by(Movie.rating.desc()).paginate(
        page,
        per_page=current_app.config.get('FLASK_MOVIE_PER_PAGE_COUNT'),
        error_out=True
    )
    movies = pagination.items

    return render_template('main/show-all-tags.html',
                           tags=tags,
                           movies=movies,
                           pagination=pagination)


@main.route('/<tag>/movies/')
def show_tag_movies(tag):
    """
    标签下的电影
    :param tagname:
    :return:
    """
    tags = Tag.query.order_by(Tag.addtime.desc()).all()
    tag = Tag.query.filter(Tag.name == tag).first()
    page = request.args.get('page', 1, type=int)
    pagination = tag.movies.order_by(Movie.rating.desc()).paginate(
        page,
        per_page=current_app.config.get('FLASK_MOVIE_PER_PAGE_COUNT'),
        error_out=True
    )
    movies = pagination.items

    return render_template('main/show-tag-movies.html',
                           tag=tag,
                           tags=tags,
                           pagination=pagination,
                           movies=movies)


@main.route('/movie/<id>', methods=['POST', 'GET'])
def movie(id):
    """
    电影信息页面
    :param id:
    :return:
    """
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated or not current_user.can(Permission.COMMENT):
            flash('您需要登录后才可以评论哦！')
            return redirect(url_for('auth.login'))
        comment = Comment(body=form.body.data,
                          movie_id=id,
                          user_id=current_user.id,
                          addtime=datetime.now())
        db.session.add(comment)
        db.session.commit()
        flash('评论已提交,谢谢分享!')
        return redirect(url_for('main.movie', id=id))

    movie = Movie.query.get_or_404(id)
    page = request.args.get('page', 1, int)
    pagination = movie.comments.order_by(Comment.addtime.desc()).paginate(
        page,
       per_page=current_app.config['FLASK_COMMENT_PER_PAGE_COUNT'],
       error_out=True
    )
    comments = pagination.items
    tags = '/'.join([tag.name for tag in movie.tags.all()])
    return render_template('main/movie.html',
                           movie=movie,
                           tags=tags,
                           form=form,
                           comments=comments,
                           pagination=pagination)


@main.route('/movie/play/<id>', methods=['POST', 'GET'])
def play_movie(id):
    """
    播放电影
    :param id:
    :return:
    """
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated or not current_user.can(Permission.COMMENT):
            flash('您需要登录后才可以评论哦！')
            return redirect(url_for('auth.login'))
        comment = Comment(body=form.body.data,
                          movie_id=id,
                          user_id=current_user.id,
                          addtime=datetime.now())
        db.session.add(comment)
        db.session.commit()
        flash('评论已提交,谢谢分享!')
        return redirect(url_for('main.play_movie', id=id))

    movie = Movie.query.get_or_404(id)
    # 增加一次播放次数
    movie.play_num += 1
    db.session.add(movie)
    db.session.commit()
    # 电影评论分页
    page = request.args.get('page', 1, int)
    pagination = movie.comments.order_by(Comment.addtime.desc()).paginate(
        page,
        per_page=current_app.config['FLASK_COMMENT_PER_PAGE_COUNT'],
        error_out=True
    )
    comments = pagination.items
    return render_template('main/play-movie.html',
                           movie=movie,
                           form=form,
                           comments=comments,
                           pagination=pagination)


@main.route('/movie/<int:id>/save-dm/')
@login_required
def save_dm(id):
    pass


@main.route('/movie/play/style.xml/')
def load_ckplayer_style_file():
    return render_template('main/style.xml')


@main.route('/movie/play/language.xml/')
def load_ckplayer_language_file():
    return render_template('main/language.xml')


@main.route('/crossdomain.xml/')
def load_ckplayer_crossdomain_file():
    return render_template('main/../../crossdomain.xml')


@main.route('/user/<id>/')
@login_required
def user(id):
    """
    显示用户信息
    :param username:
    :return:
    """
    user = User.query.filter_by(id=id).first()
    if not user:
        abort(404)

    # 电影日志
    userlog = user.userlogs.order_by(Userlog.log_time.desc())[1]
    moviecols = [moviecol.movie for moviecol in user.moviecols]

    # 所有的评论
    comments = current_user.comments

    # 关注的用户
    followeds = user.followed.all()
    # 关注你的用户
    followers = user.followers.all()

    return render_template('main/user.html',
                           user=user,
                           last_userlog=userlog,
                           moviecols=moviecols,
                           comments=comments,
                           followeds=followeds,
                           followers=followers)


@main.route('/user/<id>/editprofile/', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    """
    修改个人资料
    :param id:
    :return:
    """
    user = User.query.get_or_404(id)
    if current_user != user:
        flash('您没有权限修改他人资料!')
        return redirect(url_for('mian.user', id=id))
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.info = form.info.data
        try:
            db.session.add(current_user)
            db.session.commit()
        except:
            flash('修改失败，可能用户名被注册过！')
            db.session.rollback()
            return redirect(url_for('main.edit_profile', id=current_user.id))
        flash('资料修改成功！')
        return redirect(url_for('main.user', id=id))
    form.username.data = current_user.username
    form.info.data = current_user.info

    return render_template('main/edit-profile.html', form=form)


@main.route('/user/editpassword/', methods=['GET', 'POST'])
@login_required
def edit_password():
    """
    修改个人密码
    :return:
    """
    form = EditPasswordForm()
    if form.validate_on_submit():
        current_user.password = form.new_pwd.data
        db.session.add(current_user)
        db.session.commit()
        flash('密码重置完成！请牢记新密码！')
        return redirect(url_for('main.user', id=current_user.id))

    return render_template('main/edit-password.html', form=form)


@main.route('/moviecol/<int:id>')
@login_required
def movie_col(id):
    """
    电影收藏功能
    :param id: 电影id
    :return:
    """
    moviecol = Moviecol.query.filter_by(user_id=current_user.id).filter(Moviecol.movie_id==id).first()
    print(moviecol)
    if moviecol is not None:
        flash('您已经收藏过该电影了!')
        return redirect(url_for('main.movie', id=id))
    moviecol = Moviecol(addtime=datetime.now(),
                        user_id=current_user.id,
                        movie_id=id)
    db.session.add(moviecol)
    db.session.commit()
    flash('电影收藏成功, 您可以在收藏夹查看!')
    return redirect(url_for('main.movie', id=id))


@main.route('/user/userlog/')
@login_required
def userlog():
    """
    用户登录日志功能
    :return:
    """
    page = request.args.get('page', 1, int)
    pagination = Userlog.query.filter(Userlog.user_id==current_user.id).order_by(Userlog.log_time.desc()).paginate(
        page,
        per_page=current_app.config['FLASK_USERLOG_PER_PAGE_COUNT'],
        error_out=True
    )
    userlogs = pagination.items
    return render_template('main/userlog.html',
                           userlogs=userlogs,
                           pagination=pagination)


@main.route('/serch/movie')
def serch_movie():
    """
    搜索电影功能
    :return:
    """
    key_movie = request.args.get('key_movie', '')
    movies = Movie.query.filter(or_(Movie.name.like('%{}%'.format(key_movie)), Movie.actors.like('%{}%'.format(key_movie)))).all()
    movies_count = Movie.query.filter(or_(Movie.name.like('%{}%'.format(key_movie)), Movie.actors.like('%{}%'.format(key_movie)))).count()
    if 'auth/admin/' in request.environ.get('HTTP_REFERER', None):
        return render_template('auth/manage-movie.html',
                                   movies=movies,
                                   key_movie=key_movie,
                                   movies_count=movies_count)
    else:
        return render_template('main/serch-movie.html',
                           movies=movies,
                           key_movie=key_movie,
                           movies_count=movies_count)


@main.route('/follow/user/<int:id>/')
@login_required
def follow(id):
    """
    关注功能
    :param id:
    :return:
    """
    user = User.query.filter_by(id=id).first()
    if user:
        current_user.follow(user)
    flash('成功关注了{}'.format(user.username))
    return redirect(url_for('main.user', id=id))


@main.route('/unfollow/user/<int:id>/')
@login_required
def unfollow(id):
    """
    被关注
    :param id:
    :return:
    """
    user = User.query.filter_by(id=id).first()
    if user:
        current_user.unfollow(user)
    flash('您成功取消关注{}'.format(user.username))
    return redirect(url_for('main.user', id=id))



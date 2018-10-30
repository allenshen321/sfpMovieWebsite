from . import main
from app import db
from flask import render_template, request, current_app, abort, flash, url_for, redirect
from app.models import Movie, Tag, User
from flask_login import login_required, current_user
from .forms import EditProfileForm


@main.route('/')
def index():
    """显示首页"""
    movies = Movie.query.order_by(Movie.rating.desc()).limit(20).all()
    tags = Tag.query.all()
    return render_template('main/index.html',
                           movies=movies,
                           tags=tags)


@main.route('/show/all/movies')
def show_all_movies():
    """显示所有电影"""
    page = request.args.get('page', 1, type=int)
    pagination = Movie.query.order_by(Movie.rating.desc()).paginate(
        page,
        per_page=current_app.config.get('FLASK_MOVIE_PER_PAGE_COUNT'),
        error_out=True
    )
    movies = pagination.items

    return render_template('main/show-all-movies.html',
                           movies=movies,
                           pagination=pagination)


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
    :param tag:
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


@main.route('/movie/<id>')
def movie(id):
    """
    电影信息页面
    :param id:
    :return:
    """
    movie = Movie.query.filter_by(id=id).first()
    tags = '/'.join([tag.name for tag in movie.tags.all()])
    return render_template('main/movie.html',
                           movie=movie,
                           tags=tags)


@main.route('/movie/play/<id>')
def play_movie(id):
    """
    播放电影
    :param id:
    :return:
    """
    movie = Movie.query.filter_by(id=id).first()
    return render_template('main/play-movie.html',
                           movie=movie)


@main.route('/user/<id>/')
def user(id):
    """
    显示用户信息
    :param username:
    :return:
    """
    user = User.query.filter_by(id=id).first()
    if not user:
        abort(404)

    return render_template('main/user.html', user=user)


@main.route('/user/<id>/editprofile/', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    user = User.query.get_or_404(id)
    if current_user != user:
        flash('您没有权限修改他人资料!')
        return redirect(url_for('mian.user', id=id))
    form = EditProfileForm()
    if form.validate_on_submit():
        # is_exist_username = User.query.filter_by(username=form.username.data).first()
        # if is_exist_username:
        #     flash('用户名已经被注册了，请试试其他的！！')
        #     return redirect(url_for('main.edit_profile', id=id))
        current_user.username = form.username.data
        current_user.info = form.info.data
        try:
            db.session.add(current_user)
            db.session.commit()
        except:
            flash('修改失败，可能用户名被注册过！')
            db.session.rollback()
        flash('资料修改成功！')
        return redirect(url_for('main.user', id=id))
    form.username.data = current_user.username
    form.info.data = current_user.info

    return render_template('main/edit-profile.html', form=form)
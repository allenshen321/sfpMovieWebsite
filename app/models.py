# 定义前台模型文件，包括user、movie、tag、comment、moviecol、userlog

from flask import current_app
from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS


@login_manager.user_loader
def load_user(user_id):
    """
    flask-login加载用户的回调函数
    :param user_id:
    :return:
    """
    return User.query.get(int(user_id))


class Follows(db.Model):
    """
    用户关注关系表
    """
    __tablename__ = 'follows'

    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    addtime = db.Column(db.DateTime, default=datetime.now())


# 用户模型
class User(db.Model, UserMixin):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    username = db.Column(db.String(64), unique=True)  # 昵称，唯一
    password_hash = db.Column(db.String(255))  # 保存用户哈希密码
    email = db.Column(db.String(64), unique=True)  # 用户邮箱
    confirm = db.Column(db.Boolean, default=False)  # 是否进行邮箱确认
    info = db.Column(db.Text)  # 个人简介
    photo = db.Column(db.String(255))  # 头像
    registration_time = db.Column(db.DATETIME(), default=datetime.now())  # 注册时间
    # last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    # 用户关系
    userlogs = db.relationship('Userlog', backref='user', lazy='dynamic')  # 用户登录日志
    comments = db.relationship('Comment', backref='user', lazy='dynamic')  # 用户-评论关系
    moviecols = db.relationship('Moviecol', backref='user')  # 用户-收藏关系
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 用户角色id
    # 关注和被关注关联
    followed = db.relationship('Follows',
                               foreign_keys=[Follows.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follows',
                                foreign_keys=[Follows.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        if not self.role:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            else:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %s>' % self.username

    @property
    def password(self):
        """设置密码为只读属性"""
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, password):
        """对密码加密"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def ping(self):
        """
        刷新最后登录日期
        :return:
        """
        self.last_seen = datetime.now()

    def generate_confirm_token(self, expiration=60*20):
        """
        生成期限是20分钟的验证令牌
        :param expiration: 过期时间20分钟
        :return:
        """
        s = TJWSS(current_app.config['SECRET_KEY'], expiration=expiration)
        return s.dumps({'confirm': self.id})

    def confirm_token(self, token):
        """
        验证token
        :param token:
        :return:
        """
        s = TJWSS(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        return True

    def can(self, permissions):
        """
        验证权限
        :param permissions: 权限
        :return: Boolean
        """
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        """
        判断是否有管理员权限
        :return:
        """
        return self.can(Permission.ADMINISTER)

    def is_following(self, user):
        """
        判断是否正在关注
        :param user:
        :return:
        """
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        """
        判断是否被user关注
        :param user:
        :return:
        """
        return self.followers.filter_by(follower_id=user.id).first() is not None

    def follow(self, user):
        """
        关注用户
        :param user:
        :return:
        """
        if not self.is_following(user):
            f = Follows(followed_id=user.id,
                        follower=self,
                        addtime=datetime.now())
            db.session.add(f)
            db.session.commit()

    def unfollow(self, user):
        """
        取消关注
        :param user:
        :return:
        """
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()


class AnonymousUser(AnonymousUserMixin):
    """定义未登录用户权限验证的类"""
    def can(self, permissions):
        """权限验证"""
        return False

    def is_administrator(self):
        return False


# 设置未登录用户的current_user的值
login_manager.anonymous_user = AnonymousUser


class Userlog(db.Model):
    """用户日志模型"""
    __tablename__ = 'userlogs'

    id = db.Column(db.Integer, primary_key=True)  # 日志id
    log_time = db.Column(db.DateTime)  # 登录时间
    ip = db.Column(db.String(64))  # 登录的ip地址
    logout_time = db.Column(db.DateTime)  # 用户退出登录时间

    # 添加外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 外连用户

    def __repr__(self):
        return '<Userlog %s>' % self.id


# 电影-标签关系表
movie_tag = db.Table('movie_tag',
                     db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Movie(db.Model):
    """电影模型"""
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), unique=True)  # 电影名
    url = db.Column(db.String(1000), unique=True)  # 电影链接
    release_time = db.Column(db.String(64))  # 上映时间
    area = db.Column(db.String(64))  # 上映地区
    language = db.Column(db.String(64))  # 语言
    introduction = db.Column(db.Text)  # 电影简介
    actors = db.Column(db.String(255))  # 电影演员
    director = db.Column(db.String(125))  # 电影导演
    file_size = db.Column(db.String(64))  # 文件大小
    rating = db.Column(db.Float)  # 评分
    cover = db.Column(db.String(255))  # 电影封面
    play_num = db.Column(db.BigInteger, default=0)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论量
    is_recomment = db.Column(db.Boolean, default=False)
    addtime = db.Column(db.Date)  # 添加时间

    # 设置电影－标签外键
    comments = db.relationship('Comment', backref='movie', lazy='dynamic')  # 电影-评论关系
    moviecols = db.relationship('Moviecol', backref='movie', lazy='dynamic')  # 电影-收藏关系
    tags = db.relationship('Tag',
                           secondary='movie_tag',
                           backref=db.backref('movies', lazy='dynamic'),
                           lazy='dynamic')

    def is_recommenting(self):
        """
        判断电影是否是推荐电影
        :param movie_id:
        :return:
        """
        return self.is_recomment

    def recomment(self):
        """
        推荐电影
        :param movie_id:
        :return:
        """
        if not self.is_recomment:
            self.is_recomment = True
            db.session.add(self)
            db.session.commit()

    def unrecomment(self):
        """
        取消推荐电影
        :param movie_id:
        :return:
        """
        if self.is_recomment:
            self.is_recomment = False
            db.session.add(self)
            db.session.commit()

    @classmethod
    def delete(cls, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()


    def __repr__(self):
        return '<Movie %s>' % self.name


class Tag(db.Model):
    """电影标签模型"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)  # 标签id
    name = db.Column(db.String(64), unique=True)  # 标签名，唯一
    addtime = db.Column(db.DateTime(), default=datetime.now())  # 标签添加时间

    def __repr__(self):
        return '%s' % self.name


class Comment(db.Model):
    """评论模型"""
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)  # 评论ｉｄ
    body = db.Column(db.Text)  # 评论内容
    addtime = db.Column(db.DateTime(), default=datetime.now())  # 时间

    # 外键
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))  # 评论电影id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 评论用户id

    def __repr__(self):
        return '<Comment %s>' % self.id


class Moviecol(db.Model):
    """电影收藏模型"""
    __tablename__ = 'moviecols'

    id = db.Column(db.Integer, primary_key=True)  # 收藏id
    addtime = db.Column(db.DateTime(), default=datetime.now())  # 时间

    # 关系
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 用户-收藏关系
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))  # 电影收藏关系

    def __repr__(self):
        return '<Moviecol %s>' % self.id


class Role(db.Model):
    """
    角色模型
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)  # 角色名称
    default = db.Column(db.Boolean, index=True, default=False)
    permissions = db.Column(db.Integer)

    # 外键user-role
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %s>' % self.name

    @staticmethod
    def insert_roles():
        """
        向表roles 中添加角色
        :return:
        """
        roles = {
            'User': (Permission.WATCHING | Permission.COMMENT | Permission.DOWNLOAD, True),
            'Administrator': (Permission.WATCHING |
                          Permission.COMMENT |
                          Permission.MODERATE_COMMENTS |
                          Permission.DOWNLOAD,
                          False),
            'SuperAdministrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if not role:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    """
    权限系统
    """
    WATCHING = 0X01  # 0b00000001 观看电影
    COMMENT = 0X02   # 0b00000010 发表评论
    DOWNLOAD = 0X04  # 0b00000100 下载电影
    MODERATE_COMMENTS = 0X16  # 0b00010000 修改评论
    ADMINISTER = 0X80  # 0b10000000 超级管理员


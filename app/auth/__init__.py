# 用户认证蓝图

from flask import Blueprint

auth = Blueprint('auth', __name__)


from . import views

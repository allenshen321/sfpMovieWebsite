# 注册main蓝本

from flask import Blueprint
from app.models import Permission


main = Blueprint('main', __name__)


# 将models.py中的Permission类加入全局变量中，这样模板中可以访问
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


from . import views, errors

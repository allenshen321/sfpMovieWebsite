# 定义装饰器

from functools import wraps
from flask_login import current_user
from flask import abort
from app.models import Permission


# 定义权限要求的修饰器
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return inner
    return decorator


# 验证管理员权限修饰器
def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

"""
"""
from functools import wraps
from flask import session, abort, current_app
from app.models.user_models import (
    db, User, UsersRoles, Permissions, Role,
    RolesPermissions)



def permission_required(permission):
    """
    权限认证装饰器
    :param permission:
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                current_user = User.query.filter_by(id=session.get('_user_id')).first()
                app_name = current_app.config.get("APP_NAME")
                if not current_user or not permission_can(current_user, permission, app_name):
                    abort(403)
                return f(*args, **kwargs)
            except:
                abort(403)
        return decorated_function
    return decorator



def permission_can(current_user, permission, app_name):
    """
    检测用户是否有特定权限
    :param current_user
    :param permission
    :return:
    """
    if current_user.username == "admin":
        return True
    roles = current_user.roles
    permission_names = []
    for role in roles:
        if role.app_name != app_name:
            continue
        permissions = role.permissions
        permission_names.extend([item.name for item in permissions])
    print(permission_names)
    if permission in permission_names:
        return True
    return False


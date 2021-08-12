"""
用户管理
"""
from flask_mail import Mail
from flask_babel import Babel
from flask_admin import Admin
from ng_risk_core import config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin.base import MenuLink
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from okash_py_utils.utils.decorators import latency
from flask_user import UserManager, SQLAlchemyAdapter, current_user
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.utils import permission_required



import os.path as op
from app.models.user_models import User, UserProfileForm
from app.models.models import (
    AdmUsers, AdmUsersRoles, AdmRoles,
    AdmPermissions, AdmRolesPermissions,
    AdminUserView, AdmPermissionsView,
    AdmRolesPermissionsView, AdmUsersRolesView,
    AdmRolesView
    )


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:rootroot@localhost:3306/test"
app.secret_key = "secret"
app.config.from_mapping(
    USER_APP_NAME = 'app',
    USER_ENABLE_CHANGE_PASSWORD = True,
    USER_ENABLE_CHANGE_USERNAME = False,
    USER_ENABLE_CONFIRM_EMAIL = False,
    USER_ENABLE_FORGOT_PASSWORD = True,
    USER_ENABLE_EMAIL = False,
    USER_ENABLE_REGISTRATION = True,
    USER_ENABLE_RETYPE_PASSWORD = True,
    USER_ENABLE_USERNAME = True,
    USER_AFTER_LOGIN_ENDPOINT = 'admin.index',
    USER_AFTER_LOGOUT_ENDPOINT = 'home_page'
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_RECORD_QUERIES"] = True
app.config["SQLALCHEMY_POOL_SIZE"] = 1022
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 90
app.config["SQLALCHEMY_POOL_RECYCLE"] = 3
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 1022

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'user.login'
login_manager.login_message = "请登录"
login_manager.login_message_category = "info"
login_manager.init_app(app)
bootstrap = Bootstrap(app)

db = SQLAlchemy()
csrf_protect = CSRFProtect()
mail = Mail()
migrate = Migrate()
babel = Babel()
db_adapter = SQLAlchemyAdapter(db,User)
user_manager = UserManager(db_adapter, app)

db.init_app(app)
migrate.init_app(app, db)
mail.init_app(app)

admin = Admin(app, template_mode='bootstrap3')
admin.add_view(AdminUserView(AdmUsers, db.session, name='Users'))
admin.add_view(AdmRolesView(AdmRoles, db.session, name='Role'))
admin.add_view(AdmUsersRolesView(AdmUsersRoles, db.session, name='Roles-User'))
admin.add_view(AdmPermissionsView(AdmPermissions, db.session, name='Permission'))
admin.add_view(AdmRolesPermissionsView(AdmRolesPermissions, db.session, name='Permissions-Role'))
path = op.join(op.dirname(__file__), 'static')
admin.add_link(MenuLink(name='Profile', endpoint='user.profile'))
admin.add_link(MenuLink(name='退出', endpoint='user.logout'))


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


auth = Blueprint('auth', __name__)

@auth.before_app_request
def before_request():
    if request.path.startswith('/admin'):
        if current_user.is_authenticated:
            if not current_user.has_role("admin"):
                return redirect(url_for('user.logout'))
        else:
            return redirect(url_for('user.login'))


app.register_blueprint(auth, url_prefix='/auth')


@app.route('/')
@auth.route('/')
def home_page():
    return redirect(url_for('control_center'))


@app.route('/control-center', methods=['GET'])
@login_required
@permission_required('manual_control_center')
def control_center():
    """
    控制中心页面
    """
    return render_template('control_center.html')


if __name__ == "__main__":
    app.run(debug=True)
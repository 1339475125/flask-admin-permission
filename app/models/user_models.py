from flask_user import UserMixin
from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# Define the User data model. Make sure to add the flask_user.UserMixin !!


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False,
                      server_default=u'', unique=True)
    username = db.Column(db.Unicode(255), nullable=False,
                      server_default=u'', unique=True)
    created_time = db.Column(db.DateTime())
    updated_time = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    authenticated = db.Column('is_authenticated', db.Boolean(), nullable=False, server_default='0')
    # User information
    active = db.Column('is_active', db.Boolean(),
                       nullable=False, server_default='1')
    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))
    def is_authenticated(self):
        return self.is_authenticated

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        if User.get('id') == user_id:
            return User(user_id)
        return None



# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False,
                     server_default=u'', unique=True)  # for @roles_accepted()
    # for display purposes
    label = db.Column(db.Unicode(255), server_default=u'')
    app_name = db.Column(db.String(50), nullable=False, server_default=u'')
    permissions = db.relationship('Permissions', secondary='roles_permissions',
                            backref=db.backref('roles', lazy='dynamic'))


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'))


# Define the permissions model
class Permissions(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False,
                     server_default=u'', unique=True)  # for @roles_accepted()
    # for display purposes
    active = db.Column('is_active', db.Boolean(),
                       nullable=False, server_default='1')
    created_time = db.Column(db.DateTime())
    updated_time = db.Column(db.DateTime())


# Define RolesPermissions association model
class RolesPermissions(db.Model):
    __tablename__ = 'roles_permissions'
    id = db.Column(db.Integer(), primary_key=True)
    permission_id = db.Column(db.Integer(), db.ForeignKey(
        'permissions.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'))


# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    pass


# Define the User profile form
class UserProfileForm(FlaskForm):
    pass
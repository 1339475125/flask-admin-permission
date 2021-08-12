
from wtforms.fields import HiddenField
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView



db = SQLAlchemy()


class AdmUsers(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False,
                      server_default=u'')
    username = db.Column(db.Unicode(255), nullable=False,
                      server_default=u'', unique=True)
    created_time = db.Column(db.DateTime())
    updated_time = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    is_authenticated = db.Column(db.Boolean(), nullable=False, server_default='1')
    # User information
    active = db.Column('is_active', db.Boolean(),
                       nullable=False, server_default='0')

    def __str__(self):
        return '{}-{}'.format(self.id, self.username)


class AdmUsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    user = db.relationship('AdmUsers', backref=db.backref('users_roles', lazy='dynamic'))
    role = db.relationship('AdmRoles', backref=db.backref('users_roles', lazy='dynamic'))



class AdmRoles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False,
                     server_default=u'', unique=True)
    # for display purposes
    label = db.Column(db.Unicode(255), server_default=u'')
    app_name = db.Column(db.Unicode(50), server_default=u'')

    def __str__(self):
        return '{}-{}'.format(self.id, self.name)



class AdmPermissions(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False,
                     server_default=u'', unique=True)

    def __str__(self):
        return '{}-{}'.format(self.id, self.name)



class AdmRolesPermissions(db.Model):
    __tablename__ = 'roles_permissions'
    id = db.Column(db.Integer(), primary_key=True)
    permission_id = db.Column(db.Integer(), db.ForeignKey('permissions.id'))
    permission = db.relationship('AdmPermissions', backref=db.backref('roles_permissions', lazy='dynamic'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    role = db.relationship('AdmRoles', backref=db.backref('roles_permissions', lazy='dynamic'))


# admin view model settings
class AdminUserView(ModelView):
    can_create = False
    column_display_pk = True
    column_exclude_list = ('password')
    form_overrides = dict(password=HiddenField)
    column_searchable_list = ['username', 'email']
    column_sortable_list = ('id', )


class AdmUsersRolesView(ModelView):
    column_display_pk = True
    column_sortable_list = ('id', )
    column_hide_backrefs = False
    column_list = ["id", "user_id", "user.username", "role_id", "role.name"]
    column_searchable_list = ['user.username', 'role.name']
    form_ajax_refs = {
        'user': {
            'fields': ['id', 'username'],
            'page_size': 10
        },
        'role': {
            'fields': ['id', 'name'],
            'page_size': 10
        }
    }

class AdmRolesView(ModelView):
    column_display_pk = True
    column_sortable_list = ('id', )
    column_searchable_list = ['id', 'name']


class AdmPermissionsView(ModelView):
    column_display_pk = True
    column_sortable_list = ('id', )
    column_searchable_list = ['id', 'name']


class AdmRolesPermissionsView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ["id", "permission_id", "permission.name", "role_id", "role.name"]
    column_sortable_list = ('id', )
    column_searchable_list = ['permission.name', 'role.name']
    form_ajax_refs = {
        'permission': {
            'fields': ['id', 'name'],
            'page_size': 10
        },
        'role': {
            'fields': ['id', 'name'],
            'page_size': 10
        }
    }

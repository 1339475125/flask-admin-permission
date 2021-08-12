# -*- coding:utf-8 -*-
"""
初始化权限列表
"""
import datetime
from perm_settings import *
from flask_script import Manager, Command
from app.models.user_models import db,  User, Role, Permissions
from app.app import app
from sqlalchemy.exc import IntegrityError


manager = Manager(app)


class init_permissions(Command):
    """
    创建初始化权限数据
    """

    def run(self):
        perms = PERMS_LIST.keys()
        role = Role.query.filter(Role.name == "admin").first()
        for perm in perms:
            now = datetime.datetime.now()
            permission = Permissions(name=perm, created_time=now, updated_time=now)
            try:
                db.session.add(permission)
                role.permissions.append(permission)
                db.session.commit()
            except IntegrityError as e:
                logger.log.info(str(e))
                db.session.rollback()

            
class init_admin_user(Command):
    """
    创建初始化admin管理员数据
    """

    def run(self):
        admin_role = self.find_or_create_role('admin', 'Admin')
        # 注意自己修改密码
        self.find_or_create_user('admin', 'admin@example.com', '123456', admin_role)
        self.find_or_create_user('member', 'member@example.com', '123456')
        db.session.commit()

    def find_or_create_role(self, name, label):
        """ Find existing role or create new role """
        role = Role.query.filter(Role.name == name).first()
        if not role:
            role = Role(name=name, label=label)
            db.session.add(role)
        return role

    def find_or_create_user(self, username, email, password, role=None):
        """ Find existing user or create new user """
        user = User.query.filter(User.username == username).first()
        if not user:
            user = User(email=email,
                        username=username,
                        password=app.user_manager.hash_password(password),
                        active=1,
                        created_time=datetime.datetime.now(),
                        updated_time=datetime.datetime.now(),
                        authenticated=True if username=="admin" else False)
            if role:
                user.roles.append(role)
            db.session.add(user)
        return user
        


manager.add_command('init_admin_user', init_admin_user())
manager.add_command('init_permissions', init_permissions())


if __name__ == "__main__":
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:rootroot@localhost:3306/test"
    manager.run()
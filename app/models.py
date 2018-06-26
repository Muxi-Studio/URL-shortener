# coding: utf-8

import base64
from app import db
from flask import current_app
from datetime import datetime
from itsdangerous import URLSafeSerializer as Serializer
# from itsdangerous import TimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash


# def generate_confirmation(self):
#     s = TimedSerializer(current_app.secret_key, 'confirmation')
#     return s.dumps(self.id)
#
# def check_confirmation(self, token, max_age=3600):
#     s = TimedSerializer(current_app.secret_key, 'confirmation')
#     return s.loads(token, max_age=max_age) == self.id


class Permission:
    """
    Permission 权限
    1. COMMENT: 0x01
    2. MODERATE_COMMENTS: 0x02
    3. ADMINISTER: 0x04
    """
    COMMENT = 0x01
    MODERATE_COMMENTS = 0x02
    ADMINISTER = 0x04


class Role(db.Model):
    """
    Role: 用户角色
    1. User: COMMENT
    2. Moderator: MODERATE_COMMENTS
    3. Administrator: ADMINISTER
    :func insert_roles: 创建用户角色, 默认是普通用户
    """
    __tablename__ = 'roles'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role',
            lazy='dynamic', cascade='all')

    @staticmethod
    def insert_roles():
        """
        由于角色比较少，这里重点需要保证各个角色添加到数据库
        中的顺序一致，所以这里使用的是list，而没有用dict
        """
        roles = [
            ['User',(Permission.COMMENT, True)],
            ['Moderator', (Permission.COMMENT |
                          Permission.MODERATE_COMMENTS, False)],
            ['Administrator', (
                Permission.COMMENT |
                Permission.MODERATE_COMMENTS |
                Permission.ADMINISTER,
                False
            )]
        ]
        for r in roles:
            role = Role.query.filter_by(name=r[0]).first()
            if role is None:
                role = Role(name=r[0])
            role.permissions = r[1][0]
            role.default = r[1][1]
            db.session.add(role)
            db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"mysql_charset": "utf8"}
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(20))
    password_hash=db.Column(db.String(128))
    is_confirmed=db.Column(db.Boolean,default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    urlmaps = db.relationship('URLMapping', backref='user',
                lazy='dynamic', cascade='all')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        # 这里是要求前端将用户的密码进行base64编码
        password_decode = base64.b64decode(password)
        self.password_hash = generate_password_hash(password_decode)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self):
        """generate a token"""
        s = Serializer(
            current_app.config['SECRET_KEY']
            # expiration
        )
        return s.dumps({'id': self.id})

    def generate_confirmation_token(self):
        """generate a tkoen for confirmation"""
        s=Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({"confirm":self.id})



    def to_json(self):
        json_user = {
            'id': self.id,
            'email': self.email,
            'is_confirmed': self.is_confirmed,
            'role_id': self.role_id
        }
        return json_user

    @staticmethod
    def verify_auth_token(token):
        """verify the user with token"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        # get id
        return User.query.get_or_404(data['id'])

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        # is administrator
        return (self.role_id == 3)

    def __repr__(self):
        return '<User %r>' % self.email


class AnonymousUser():
    """
    AnonymousUser: 匿名用户
    :func can:
        权限判断, 匿名用户没有任何权限
    :func is_administrator:
        是否是管理员, 返回False
    :generate_auth_token:
        生成验证token, 匿名用户没有id, 不生成token
    """
    __table_args__ = {'mysql_charset': 'utf8'}

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def generate_auth_token(self, ):
        return None



class URLMapping(db.Model):
    __tablename__ = "urlmaps"
    __table_args__ = {"mysql_charset": "utf8"}
    id=db.Column(db.Integer,primary_key=True)
    long_url=db.Column(db.String(200),unique=True,index=True)
    short_code=db.Column(db.String(20),unique=True,index=True)
    id_used=db.Column(db.Boolean,default=True)
    item_type=db.Column(db.String,default="generated") #默认为generated，如果传来自定义短码则为custom
    insert_time=db.Column(db.DateTime,default=datetime.utcnow)
    update_time=db.Column(db.DateTime,default=datetime.utcnow)
    available=db.Column(db.Boolean,default=True)
    is_locked=db.Column(db.Boolean,default=False)
    password=db.Column(db.String(50),nullable=True)
    count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    statistics = db.relationship('Statistics', backref='urlmap',
                              lazy='dynamic', cascade='all')

    def to_json(self):
        json_URLMap = {
            'id': self.id,
            'long_url': self.long_url,
            'short_url': self.short_code,
            'item_type':self.item_type,
            'available':self.available,
            'is_locked':self.is_locked,
            'password':self.password,
            'count':self.count,
            'user_id':self.user_id
        }
        return json_URLMap

    def __repr__(self):
        return '<URLMapping %r>' % self.long_url

class Statistics(db.Model):
    __tablename__ = "statistics"
    __table_args__ = {"mysql_charset": "utf8"}
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    useragent=db.Column(db.String(200))
    ip=db.Column(db.String(50))
    urlmap_id=db.Column(db.Integer,db.ForeignKey("urlmaps.id"))


    def to_json(self):
        json_statistics = {
            'id': self.id,
            'timestamp': self.timestamp,
            'useragent': self.useragent,
            'item_type':self.item_type,
            'ip':self.ip
        }
        return json_statistics

    def __repr__(self):
        return '<Statistics %r>' % self.long_url
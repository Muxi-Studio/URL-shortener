import base64
from app import db
from flask import current_app
from datetime import datetime
from itsdangerous import URLSafeSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash


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
    1. User: COMMENT id=3
    2. Moderator: MODERATE_COMMENTS id=2
    3. Administrator: ADMINISTER  id=1
    :func insert_roles: 创建用户角色, 默认是普通用户
    """
    __table_args__ = {'mysql_charset': 'utf8'}
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role',
            lazy='dynamic', cascade='all')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.COMMENT, True),
            'Moderator': (Permission.COMMENT |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (
                Permission.COMMENT |
                Permission.MODERATE_COMMENTS |
                Permission.ADMINISTER,
                False
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"mysql_charset": "utf8"}
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(20))
    password=db.Column(db.String(128))
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
        return (self.role_id == 2)

    def __repr__(self):
        return '<User %r>' % self.email


class URLMapping(db.Model):
    __tablename__ = "urlmaps"
    __table_args__ = {"mysql_charset": "utf8"}
    id=db.Column(db.Integer,primary_key=True)
    long_url=db.Column(db.String(200),unique=True,index=True)
    short_code=db.Column(db.String(20),unique=True,index=True)
    item_type=db.Column(db.Boolean,default=True)
    insert_time=db.Column(db.DateTime,default=datetime.utcnow)
    update_time=db.Column(db.DateTime,default=datetime.utcnow)
    available=db.Column(db.Boolean,default=True)
    is_locked=db.Column(db.Boolean,default=False)
    password=db.Column(db.String(20),nullable=True)
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
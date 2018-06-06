from app import db
from datetime import datetime

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
    email=db.Column(db.String(20))
    password=db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    urlmaps = db.relationship('URLMapping', backref='user',
                lazy='dynamic', cascade='all')


class URLMapping(db.Model):
    __tablename__ = "urlmaps"
    __table_args__ = {"mysql_charset": "utf8"}
    id=db.Column(db.Integer,primary_key=True)
    long_url=db.Column(db.String(200),unique=True)
    short_code=db.Column(db.String(20),unique=True)
    item_type=db.Column(db.Boolean,default=True)
    insert_time=db.Column(db.DateTime,default=datetime.utcnow)
    update_time=db.Column(db.DateTime,default=datetime.utcnow)
    avalible=db.Column(db.Boolean,default=True)
    is_locked=db.Column(db.Boolean,default=False)
    password=db.Column(db.String(20),nullable=True)
    count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    statistics = db.relationship('Statistics', backref='urlmap',
                              lazy='dynamic', cascade='all')

class Statistics(db.Model):
    __tablename__ = "statistics"
    __table_args__ = {"mysql_charset": "utf8"}
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    useragent=db.Column(db.String(200))
    ip=db.Column(db.String(50))
    urlmap_id=db.Column(db.Integer,db.ForeignKey("urlmaps.id"))



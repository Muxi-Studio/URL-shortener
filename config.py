# coding: utf-8

# project base path
import os
basedir = os.path.abspath(os.path.dirname(__file__))
"""
common configuration
 -- SECRET_KEY: secret key
 -- SQLALCHEMY_COMMIT_ON_TEARDOWN: True
 -- SQLALCHEMY_RECORD_QUERIES:
    -- Can be used to explicitly disable or enable query recording.
       Query recording automatically happens in debug or testing mode.
 -- SQLALCHEMY_TRACK_MODIFICATIONS:
    -- If set to True, Flask-SQLAlchemy will track modifications of
       objects and emit signals.
       The default is None, which enables tracking but issues a warning that
       it will be disabled by default in the future.
       This requires extra memory and should be disabled if not needed.
 more configuration keys please see:
  -- http://flask-sqlalchemy.pocoo.org/2.1/config/#configuration-keys
"""
class Config:
    """common configuration"""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.qq.com'  # 邮件服务器地址
    MAIL_PORT = 25  # 邮件服务器端口
    MAIL_USE_TLS = True  # 启用 TLS
    MAIL_USERNAME = "3480437308@qq.com"  # os.environ.get('MAIL_USERNAME') or 'me@example.com'
    MAIL_PASSWORD = "iifwjwzfjxvxchig"  # os.environ.get('MAIL_PASSWORD') or '123456'
    CELERY_BROKER_URL = os.getenv('BROKER_URL') or 'redis://127.0.0.1:6379'  # 指定 Broker
    CELERY_BACKEND_URL = os.getenv('CELERY_RESULT_BACKEND') or 'redis://127.0.0.1:6379/0'  # 指定 Backend
    @staticmethod
    def init_app(app):
        pass


"""
development configuration
 -- DEBUG: debug mode
 -- SQLALCHEMY_DATABASE_URI:
    -- The database URI that should be used for the connection.
more connection URI format:
 -- Postgres:
    -- postgresql://scott:tiger@localhost/mydatabase
 -- MySQL:
    -- mysql://scott:tiger@localhost/mydatabase
 -- Oracle:
    -- oracle://scott:tiger@127.0.0.1:1521/sidname
"""
class DevelopmentConfig(Config):
    """development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")



"""
testing configuration
 -- TESTING: True
 -- WTF_CSRF_ENABLED:
    -- in testing environment, we don't need CSRF enabled
"""
class TestingConfig(Config):
    """testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data-tests.sqlite")
    WTF_CSRF_ENABLED = False



# production configuration
class ProductionConfig(Config):
    """production configuration"""
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    "develop": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}

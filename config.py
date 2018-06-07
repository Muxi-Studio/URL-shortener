import os
basedir=os.path.dirname(os.path.abspath(__file__))

class Config (object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or "you_never_know"
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=os.environ.get("DEV_DATABASE_URL") or \
        "mysql+pymysql://root:pqc19960320@localhost:3306/shortURL"

config={
    "default":DevelopmentConfig
}
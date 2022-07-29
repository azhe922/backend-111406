import os
class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    DB_HOST = os.getenv('db_host')
    JSON_AS_ASCII = False    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('email_username')
    MAIL_PASSWORD = os.getenv('email_password')

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    DB_HOST = os.getenv('db_host')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
config = {
    'development': Config,
    'production': ProductionConfig,
    # 'heroku': HerokuConfig,

    'default': Config
}
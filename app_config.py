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

        # email errors to the administrators
        # import logging
        # from logging.handlers import SMTPHandler
        # credentials = None
        # secure = None
        # if getattr(cls, 'MAIL_USERNAME', None) is not None:
        #     credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
        #     if getattr(cls, 'MAIL_USE_TLS', None):
        #         secure = ()
        # mail_handler = SMTPHandler(
        #     mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
        #     fromaddr=cls.FLASKY_MAIL_SENDER,
        #     toaddrs=[cls.FLASKY_ADMIN],
        #     subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
        #     credentials=credentials,
        #     secure=secure)
        # mail_handler.setLevel(logging.ERROR)
        # app.logger.addHandler(mail_handler)

# class HerokuConfig(ProductionConfig):

#     @classmethod
#     def init_app(cls, app):
#         ProductionConfig.init_app(app)

#         # log to stderr
#         import logging
#         from logging import StreamHandler
#         file_handler = StreamHandler()
#         file_handler.setLevel(logging.INFO)
#         app.logger.addHandler(file_handler)


config = {
    'development': Config,
    'production': ProductionConfig,
    # 'heroku': HerokuConfig,

    'default': Config
}
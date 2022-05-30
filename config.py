class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    DB_HOST = 'mongodb+srv://backend:mtB5i2RUuWuSL2CK@cluster0.ftra1.mongodb.net/ntubapp'
    JSON_AS_ASCII = False

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    DB_HOST = 'mongodb+srv://backend:mtB5i2RUuWuSL2CK@cluster0.ftra1.mongodb.net/ntubapp'
    JSON_AS_ASCII = False
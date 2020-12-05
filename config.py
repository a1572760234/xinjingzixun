import logging

from redis import StrictRedis


class DefaultConfig(object):
    DEBUG = None

    SECRET_KEY = 'ASD;LFKJALS;EKJRSER'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost/xinjingzixun'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = 'redis'
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600

    # LOG_LEVEL = logging.DEBUG


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    pass


class ProductionConfig(DefaultConfig):
    DEBUG = False
    # LOG_LEVEL = logging.ERROR
    pass


config_dict = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig
}

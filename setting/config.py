class DefaultConfig(object):
    # mysql
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.19.128:3306/xinjingzixun'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否跟踪sql语句
    SQLALCHEMY_ECHO = False  # 是否开启mysql控制台输出

    # redis配置
    REDIS_HOST = '192.168.19.128'  # 主机
    REDIS_PORT = 6381  # 端口

    # jwt
    JWT_SECRET = 'TWRbyVqqwerdf8zu9v82dWYW17/z+UvRnYTt4P6fAXA'  # 秘钥
    JWT_EXPIRE_DAYS = 14

    # 七牛云相关配置
    QI_NIU_ACCESSKEY = None
    QI_NIU_SECRETKEY = None
    QI_NIU_DORMAINNAME = None  # 域名
    QIN_NIU_BURCKETNAME = None  # 空间名


class DevelopmentConfig(DefaultConfig):
    pass


class ProductionConfig(DefaultConfig):
    pass


config_dict = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
}

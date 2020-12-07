import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config_dict

db = SQLAlchemy()
redis_client = None


import logging
from logging.handlers import RotatingFileHandler
# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG) # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("./logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)


def register_bp(app:Flask):
    from info.modules.index import index_bp
    from info.modules.passport import passport_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(passport_bp)

def create_app(config_type):

    # 配置
    app = Flask(__name__)
    app.config.from_object(config_dict[config_type])
    # 配置数据库
    db.init_app(app)
    # 配置redis
    global redis_client
    # 不配置解码，需要解码的对象再使用decode()
    redis_client = redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])
    # 开启csrf保护
    # CSRFProtect(app)
    # 设置session保存位置
    Session(app)
    # 设置日志
    # setup_log()
    #注册蓝图
    register_bp(app)

    return app

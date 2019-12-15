# -*- coding:utf-8 -*-
# author: Steven
# datetime:2019/12/7 19:33
# software: PyCharm
# Description：配置类

import redis


class Config:
    """配置信息"""

    SECRET_KEY = "XHSsfsOI*Y9dfs9cs$%hd9"

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:16333zsh@127.0.0.1:3306/automation"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = "192.168.33.128"
    REDIS_PORT = 6379
    REDIS_PASSWORD = "16333zsh"

    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期，单位秒

    #  解决返回中文乱码
    JSON_AS_ASCII = False


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置信息"""
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}



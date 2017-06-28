import logging


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/queue.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGGING_LOCATION = 'logs/CHALLENGE.LOG'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LEVEL = logging.INFO

    CELERY_BROKER_URL = 'amqp://guest@localhost//'
    CELERY_RESULT_BACKEND = 'amqp://guest@localhost//'

    PORT = 4555
    USER_RELOADER = False
    HOST_NAME = "omiron.ro"
    THREADED = True
    PROCESSES = 1
    USE_RELOADER = True
    SECRET_KEY = 'be_water_my_friend'


class DevConfig(Config):
    Config.PORT = 4555
    Config.USER_RELOADER = False
    Config.HOST_NAME = "127.0.0.1"
    Config.LOGGING_FORMAT = ('%(asctime)s - %(name)s - '
                             '%(levelname)s - %(message)s')
    Config.LOGGING_LEVEL = logging.DEBUG
    Config.THREADED = True
    Config.PROCESSES = 1

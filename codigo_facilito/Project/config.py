import os

class Config(object):
    SECRET_KEY = 'my_secret_key'
    MAIL_SERVER =  'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL =True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'fnsk1999@gmail.com'
    MAIL_PASSWORD = 'rzqcswhcqgszyxgd'

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123@localhost/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
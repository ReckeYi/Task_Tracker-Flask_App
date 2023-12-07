import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    SECRET_KEY = os.getenv('S_K')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') #local
    # SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL') #docker
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')


class TestConfig:
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.getenv('S_K')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:asdasdasd@localhost:5432/flask_test' #local
    # SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_URL') #docker
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')

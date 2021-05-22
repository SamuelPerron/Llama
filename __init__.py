# Standard libraries
import os

import redis
from celery import Celery
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Local
from .celery_utils import init_celery

load_dotenv()

db = SQLAlchemy()

# --- ENV variables --- #
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
ALPACA_UID = os.getenv('ALPACA_UID')
ALPACA_SECRET = os.getenv('ALPACA_SECRET')
ACOUNT_BASE_CASH = os.getenv('ACOUNT_BASE_CASH')


def make_celery(app_name=__name__):
    redis_url = 'redis://redis.6379'
    return Celery(app_name, backend=redis_url, broker=redis_url)


celery = make_celery()


def create_app(env='production'):
    app = Flask(__name__)

    if env == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'SQLALCHEMY_DATABASE_URI',
            'postgresql://postgres:example@db:5432/llama',
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['CELERY_BROKER_URL'] = ('redis://redis:6379',)
        app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379'

        CORS(app)

        redis_obj = redis.StrictRedis(host='redis', port=6379, db=0)

        init_celery(celery, app)

    elif env == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'SQLALCHEMY_TEST_DATABASE_URI',
            'postgresql://test_user:somestrong@localhost:5432/test_llama',
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    # --- App imports --- #
    # Local
    from .account import Account, accounts_blueprint

    app.register_blueprint(accounts_blueprint, url_prefix='/account')

    # Local
    from .position import Position, positions_blueprint

    app.register_blueprint(positions_blueprint, url_prefix='/positions')

    # Local
    from .order import Order, orders_blueprint

    app.register_blueprint(orders_blueprint, url_prefix='/orders')

    return app

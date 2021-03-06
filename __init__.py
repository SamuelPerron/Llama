from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import redis
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

# --- ENV variables --- #
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
ALPACA_UID = os.getenv('ALPACA_UID')
ALPACA_SECRET = os.getenv('ALPACA_SECRET')
ACOUNT_BASE_CASH = os.getenv('ACOUNT_BASE_CASH')

def create_app(env='production'):  
    app = Flask(__name__)

    if env == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:example@db:5432/llama'
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

        CORS(app)

        redis_obj = redis.StrictRedis(host='redis', port=6379, db=0)

    elif env == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'SQLALCHEMY_TEST_DATABASE_URI', 'postgresql://test_user:somestrong@localhost:5432/test_llama'
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    # --- App imports --- #
    from .account import accounts_blueprint, Account
    app.register_blueprint(accounts_blueprint, url_prefix='/account')

    from .position import positions_blueprint, Position
    app.register_blueprint(positions_blueprint, url_prefix='/positions')

    from .order import orders_blueprint, Order
    app.register_blueprint(orders_blueprint, url_prefix='/orders')

    return app
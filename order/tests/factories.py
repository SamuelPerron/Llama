# Standard libraries
from datetime import datetime

import factory
import factory.fuzzy as fuzzy
from faker import Faker

# Local
from ... import db
from ...account.tests.factories import AccountFactory
from ...base import SIDES
from ...position import Position
from .. import Order

STOCK_SYMBOLS = (
    'TSLA',
    'AAPL',
    'GME',
    'NKE',
    'GS',
    'AMZN',
    'BABA',
    'NVDA',
    'GM',
)

fake = Faker()


class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Order
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = None

    account = factory.SubFactory(AccountFactory)
    symbol = fuzzy.FuzzyChoice(STOCK_SYMBOLS)
    qty = fake.random_digit_not_null()
    order_type = (
        Order.MARKET
    )  # TODO: order_type = factory.fuzzy.FuzzyChoice(Order.TYPES)
    stop_price = None
    side = fuzzy.FuzzyChoice(SIDES, getter=lambda c: c[0])
    status = Order.NEW

    class Params:
        filled = factory.Trait(status=Order.FILLED, filled_at=datetime.now())
        cancelled = factory.Trait(
            status=Order.CANCELLED, cancelled_at=datetime.now()
        )

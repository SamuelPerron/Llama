import factory
import factory.fuzzy as fuzzy
from faker import Faker

# Local
from ... import db
from ...account.tests.factories import AccountFactory
from ...base import SIDES
from ...order.tests.factories import STOCK_SYMBOLS
from .. import Position

fake = Faker()


class PositionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Position
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    account = factory.SubFactory(AccountFactory)
    symbol = fuzzy.FuzzyChoice(STOCK_SYMBOLS)
    qty = fake.random_digit_not_null()
    side = fuzzy.FuzzyChoice(SIDES, getter=lambda c: c[0])
    entry_price = fake.pyfloat(positive=True, max_value=1200)

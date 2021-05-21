from datetime import datetime

from ...base.tests import BaseTestCase
from ...base.utils import get_current_account
from ...order.tests.factories import OrderFactory
from ...position.tests.factories import PositionFactory
from .. import Account
from .factories import AccountFactory


class TestAccountModels(BaseTestCase):
    def test_equity(self):
        """
        Checks that equity returns total cash + total positions value
        It should also create an historical equity
        """
        position = PositionFactory()
        account = position.account
        base_nb_historical_equities = len(account.historical_equities)

        position_value = position.market_value()
        equity = account.equity()
        new_nb_historical_equities = len(account.historical_equities)

        assert equity == account.cash + position_value
        assert new_nb_historical_equities == base_nb_historical_equities + 1

    def test_buying_power(self):
        """
        Checks that buying_power returns total cash - frozen funds in
        open orders
        """
        account = AccountFactory()
        order = OrderFactory(account=account)
        order.save_to_db()

        cash = account.cash

        assert account.buying_power() == cash

    def test_get_equity_of_date(self):
        """
        Checks that get_equity_of_date returns
        hisorical equity of specific date
        """
        account = AccountFactory()
        equity = account.equity()

        assert account.get_equity_of_date() == None
        assert account.get_equity_of_date(datetime.now()) == equity

    def test_reset_account(self):
        """
        Checks that the account and all objects attached to it are
        archived and that a new one is created
        """
        account = AccountFactory()
        account.cash = 233
        account.save_to_db()

        base_account_id = account.id
        base_nb_account = len(Account.query.all())

        order = OrderFactory(account=account)
        position = PositionFactory(account=account)

        account.reset()

        assert account.soft_deleted is True
        assert order.soft_deleted is True
        assert position.soft_deleted is True

        assert len(Account.query.all()) == (base_nb_account + 1)

        new_account = Account.query.all()[-1]
        assert new_account.id == (base_account_id + 1)

        current_account = get_current_account()
        assert current_account == new_account

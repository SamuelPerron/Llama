# Standard libraries
from io import UnsupportedOperation

# Third party
import pytest

# Local
from ...account.tests.factories import AccountFactory
from ...base import LONG, SHORT
from ...base.tests import BaseTestCase
from ...position import Position
from ..models import (
    INSUFFICIENT_FUNDS,
    NOT_HOLDING_POSITION,
    Order,
    UnsupportedOrderType,
)
from .factories import OrderFactory


class TestOrderModels(BaseTestCase):
    def test_needed_funds_filled(self):
        """
        Checks that, when we save an order, the needed_funds field
        is filled and that the amount is substracted from the account's cash
        """
        account = AccountFactory()
        base_account_cash = account.cash
        order = OrderFactory(side=LONG, account=account)
        order.save_to_db()
        new_account_cash = account.cash

        assert order.needed_funds is not None
        assert new_account_cash == base_account_cash - order.needed_funds

    def test_create_long_order(self):
        """
        Creating an order should add it to the account orders
        and freeze the funds necessary for the execution
        """
        account = AccountFactory()
        original_cash = account.cash

        order = OrderFactory(account=account, side=LONG)
        order.save_to_db()

        assert order in account.orders
        assert account.cash == original_cash - order.needed_funds

    def test_create_short_order_without_holding_symbol(self):
        """
        This should reject the order for now
        """
        order = OrderFactory(side=SHORT)
        order.save_to_db()

        assert order.fill() == False
        assert order.status == Order.REJECTED
        assert order.rejected_cause == NOT_HOLDING_POSITION

    def test_fill_long_order(self):
        """
        This should remove the funds from the cash balance of the account
        and create the right position
        """
        account = AccountFactory(rich=True)
        original_cash = account.cash

        order = OrderFactory(side=LONG, account=account)
        order.save_to_db()

        assert order.fill() == True
        assert order.status == Order.FILLED
        assert account.cash == original_cash - (order.filled_price * order.qty)
        position = account.positions[0]
        assert position.symbol == order.symbol
        assert position.entry_price == order.filled_price
        assert order.cancel() == False

    def test_fill_long_order_insufficient_funds(self):
        """
        This shoud get rejected
        """
        account = AccountFactory(poor=True)
        original_cash = account.cash

        order = OrderFactory(side=LONG, account=account)
        order.save_to_db()

        assert order.fill() == False
        assert order.status == Order.REJECTED
        assert order.rejected_cause == INSUFFICIENT_FUNDS

    def test_fill_unsupported_order_type(self):
        """
        This shoud raise an error
        """
        order = OrderFactory(order_type=Order.STOP)
        order.save_to_db()

        with pytest.raises(UnsupportedOrderType):
            order.fill()

    def test_fill_short_order(self):
        """
        This should add the gain of the sale to the
        cash balance of the account and close the right position
        """
        account = AccountFactory(rich=True)

        long = OrderFactory(account=account, side=LONG)
        long.save_to_db()
        long.fill()
        original_cash = account.cash

        short = OrderFactory(
            account=account, side=SHORT, symbol=long.symbol, qty=long.qty
        )
        short.save_to_db()

        assert short.fill() == True
        assert short.status == Order.FILLED
        assert account.cash == original_cash + (short.filled_price * short.qty)
        assert account.positions[0].closed == True

    def test_cancel_order(self):
        """
        This should cancel the order, any subsequent attempts to
        fill the order should fail. Frozen funds should be recredited.
        """
        account = AccountFactory()
        original_cash = account.cash

        order = OrderFactory(account=account, side=LONG)
        order.save_to_db()

        assert order.cancel() == True
        assert order.status == Order.CANCELLED
        assert order.fill() == False
        assert round(account.cash) == round(original_cash)

    # # https://stackoverflow.com/questions/53590758/how-to-mock-function-call-in-flask-restul-resource-method
    # TODO
    # def test_stop_loss(self):
    #     """
    #     The order should fill when the stop price is reached
    #     """
    #     pass

# Local
from ...base import LONG, SHORT
from ...base.tests import BaseTestCase
from ...order import Order
from .factories import PositionFactory


class TestPositionModels(BaseTestCase):
    def test_close(self):
        """
        Checks that when closing a position, it creates the right order
        """
        position = PositionFactory()
        base_order_count = len(Order.query.all())

        position.close()

        last_order = Order.query.all()[-1]
        oposite_side = LONG if position.side == SHORT else SHORT

        assert len(Order.query.all()) == (base_order_count + 1)
        assert last_order.symbol == position.symbol
        assert last_order.qty == position.qty
        assert last_order.side == oposite_side

    def test_cost_basis(self):
        """
        Checks that cost_basis returns correct value
        """
        position = PositionFactory()

        assert position.cost_basis() == position.qty * position.entry_price

    def test_market_value(self):
        """
        Checks that market_value returns correct value
        """
        position = PositionFactory()
        estimated = position.qty * position.current_price()

        assert position.market_value() == estimated

    def test_unrealized_pl(self):
        """
        Checks that unrealized_pl returns correct value
        """
        position = PositionFactory()
        estimated = position.market_value() - position.cost_basis()

        assert position.unrealized_pl() == estimated

    def test_change_today(self):
        """
        Checks that change_today returns correct value
        """
        position = PositionFactory()
        estimated = position.current_price() - position.lastday_price()

        assert position.change_today() == estimated

    def test_unrealized_intraday_pl(self):
        """
        Checks that unrealized_intraday_pl returns correct value
        """
        position = PositionFactory()
        estimated = position.change_today() * position.qty

        assert position.unrealized_intraday_pl() == estimated

    def test_unrealized_intraday_plpc(self):
        """
        Checks that unrealized_intraday_plpc returns correct value
        """
        position = PositionFactory()
        cost_basis = position.cost_basis()
        estimated = round(
            (position.unrealized_intraday_pl() - cost_basis) / cost_basis, 2
        )

        assert round(position.unrealized_intraday_plpc(), 2) == estimated

    def test_current_price(self):
        """
        Checks that current_price returns a number
        """
        position = PositionFactory()

        assert type(position.current_price()) == float

    def test_lastday_price(self):
        """
        Checks that last_day_price returns a number
        """
        position = PositionFactory()

        assert type(position.lastday_price()) == float

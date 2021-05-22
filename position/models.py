# Standard libraries
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.choice import ChoiceType

# Local
from .. import db
from ..base import LONG, SHORT, SIDES, BaseDBModel
from ..base.utils import alpaca, bars


class Position(db.Model, BaseDBModel):
    __tablename__ = 'positions'

    account_id = db.Column(
        db.Integer, db.ForeignKey('accounts.id'), nullable=False
    )
    symbol = db.Column(db.String)
    qty = db.Column(db.Integer)
    side = db.Column(ChoiceType(SIDES))
    entry_price = db.Column(db.Float)
    closed = db.Column(db.Boolean, default=False)

    _current_price = db.Column(db.Float)
    _current_price_last_check = db.Column(db.DateTime)
    _lastday_price = db.Column(db.Float)
    _lastday_price_last_check = db.Column(db.DateTime)

    account = relationship(
        'Account', foreign_keys='Position.account_id', backref='positions'
    )

    def close(self):
        """
        Creates a closing order
        """
        # Local
        from ..order import Order

        side = LONG if self.side == SHORT else SHORT
        order = Order(
            account=self.account,
            symbol=self.symbol,
            qty=self.qty,
            order_type=Order.MARKET,
            side=side,
        )
        order.save_to_db()

    def cost_basis(self):
        """
        Total cost basis in dollar
        """
        return self.qty * self.entry_price

    def market_value(self):
        """
        Total dollar amount of the position
        """
        return self.qty * self.current_price()

    def unrealized_pl(self):
        """
        Unrealized profit/loss in dollars
        """
        return self.market_value() - self.cost_basis()

    def unrealized_plpc(self):
        """
        Unrealized profit/loss percent
        """
        return self.unrealized_pl() / self.cost_basis()

    def change_today(self):
        """
        Percent change from last day price
        """
        return self.current_price() - self.lastday_price()

    def unrealized_intraday_pl(self):
        """
        Unrealized profit/loss in dollars for the day
        """
        return self.change_today() * self.qty

    def unrealized_intraday_plpc(self):
        """
        Unrealized profit/loss percent for the day
        """
        cost_basis = self.cost_basis()
        return (self.unrealized_intraday_pl() - cost_basis) / cost_basis

    def current_price(self):
        """
        Current asset price per share
        """
        DELAY_IN_SECONDS = 10
        now = datetime.now()

        if (
            not self._current_price_last_check
            or (now - self._current_price_last_check).total_seconds()
            > DELAY_IN_SECONDS
        ):
            self._current_price_last_check = now

            self._current_price = alpaca(
                'get', f'last/stocks/{self.symbol}'
            ).json()['last']['price']

        return self._current_price

    def lastday_price(self):
        """
        Last day’s asset price per share based on the closing value of the last trading day
        """
        now = datetime.now()

        if (
            not self._lastday_price_last_check
            or now.date() != self._lastday_price_last_check.date()
        ):
            self._lastday_price_last_check = now

            data = bars((self.symbol,), 'day', limit=1)[self.symbol][0]
            self._lastday_price = self.current_price() - data['c']

        return self._lastday_price

    def get_public_fields():
        return BaseDBModel.get_public_fields() + (
            'symbol',
            'qty',
            'side',
        )

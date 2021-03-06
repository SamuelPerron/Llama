from datetime import datetime, timedelta

from .. import ACOUNT_BASE_CASH, db
from ..base import BaseDBModel
from ..base.utils import clock

association_table_account_historical_equities = db.Table(
    "association_account_historical_equities",
    db.Model.metadata,
    db.Column("account_id", db.Integer, db.ForeignKey("accounts.id")),
    db.Column(
        "historical_equity_id", db.Integer, db.ForeignKey("historical_equities.id")
    ),
)


class Account(db.Model, BaseDBModel):
    __tablename__ = "accounts"

    cash = db.Column(db.Float, default=0)

    historical_equities = db.relationship(
        "HistoricalEquity",
        backref="account",
        secondary=association_table_account_historical_equities,
    )

    def equity(self):
        """
        Total value of cash + holding positions
        """
        equity = self.cash + sum((p.market_value() for p in self.positions))

        historical = HistoricalEquity(timestamp=datetime.now(), equity=equity)
        historical.save_to_db()
        self.historical_equities.append(historical)
        self.save_to_db()

        return equity

    def last_equity(self):
        """
        Equity as of previous trading day at 16:00:00 ET
        """
        return self.get_equity_of_date(
            datetime.strptime(clock()["last_close"], "%Y-%m-%dT%H:%M")
        )

    def get_equity_of_date(self, date=None):
        if date is not None:
            grace_period = 5

            start_grace = date - timedelta(minutes=grace_period)
            finish_grace = date + timedelta(minutes=grace_period)

            for h in self.historical_equities:
                if h.timestamp >= start_grace and h.timestamp <= finish_grace:
                    return h.equity

        return None

    def buying_power(self):
        """
        Current available $ buying power
        """
        return self.cash

    def reset(self):
        self.delete()

        for position in self.positions:
            position.delete()

        for order in self.orders:
            order.delete()

        new_account = Account(cash=ACOUNT_BASE_CASH)
        new_account.save_to_db()

    def get_public_fields():
        return BaseDBModel.get_public_fields() + ("cash",)


class HistoricalEquity(db.Model, BaseDBModel):
    __tablename__ = "historical_equities"

    timestamp = db.Column(db.DateTime)
    equity = db.Column(db.Float)

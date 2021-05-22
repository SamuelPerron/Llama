# Local
from ...base.tests import BaseTestCase
from ...order import Order
from .factories import PositionFactory


class TestPositionViews(BaseTestCase):
    def test_positions(self):
        """
        Should return positions of current account
        """
        position = PositionFactory()

        with self.client as c:
            r = c.get('/positions/')
            assert r.status_code == 200

            assert len(r.json['data']) == 1
            assert r.json['data'][0]['id'] == position.id

    def test_close(self):
        """
        Should close the positions
        """
        positions = [PositionFactory() for _ in range(0, 4)]
        base_order_count = len(Order.query.all())

        with self.client as c:
            r = c.post(
                f'/positions/close',
                json={'ids': [position.id for position in positions]},
            )
            assert r.status_code == 200

            assert r.json['success']
            assert len(Order.query.all()) == (
                base_order_count + len(positions)
            )

    def test_close_fake_positions(self):
        """
        Should return an error
        """
        base_order_count = len(Order.query.all())

        with self.client as c:
            r = c.post(
                f'/positions/close',
                json={
                    'ids': [
                        99999,
                    ]
                },
            )
            assert r.status_code == 404

            assert len(Order.query.all()) == base_order_count

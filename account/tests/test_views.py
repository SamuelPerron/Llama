from ...base.tests import BaseTestCase
from .. import Account
from .factories import AccountFactory


class TestAccountViews(BaseTestCase):
    def test_account(self):
        """
        Should returns account
        """
        with self.client as c:
            r = c.get("/account/")
            assert r.status_code == 200

            assert r.json["data"]["id"]

    def test_reset_account(self):
        """
        Should archive old account and return new one
        """
        first_account = AccountFactory()

        with self.client as c:
            r = c.get("/account/reset_account")
            assert r.status_code == 200

            assert r.json["data"]["id"]
            assert r.json["data"]["id"] == (first_account.id + 1)

            assert first_account.soft_deleted

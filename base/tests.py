import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase

from .. import create_app, db


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app("testing")
        self.db = db
        self.client = app.test_client()

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

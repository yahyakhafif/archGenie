import pytest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from config.db import db as _db


@pytest.fixture(scope='session')
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.environ.get(
            'TEST_DATABASE_URL',
            'postgresql://localhost:5432/archgenie_test'
        ),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    app = create_app(test_config)
    return app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def init_db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()

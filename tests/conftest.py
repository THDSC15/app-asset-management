import pytest
import tempfile
import os

from app import app, db


@pytest.fixture
def client():

    db_fd, db_path = tempfile.mkstemp()

    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    with app.test_client() as client:

        with app.app_context():
            db.create_all()

        yield client

        with app.app_context():
            db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)
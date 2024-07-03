import pytest
from app import create_app, db


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    with flask_app.app_context():
        yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='module')
def init_database():
    flask_app = create_app()

    # Establish an application context before running the tests.
    with flask_app.app_context():
        # Create the database and the database table(s)
        db.create_all()

        yield db  # this is where the testing happens!

        db.session.remove()
        # Drop the database tables after the test runs
        db.drop_all()

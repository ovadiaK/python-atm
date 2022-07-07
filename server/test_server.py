from pytest_bdd import scenario, given, when, then
from pathlib import Path
import pytest

from server import create_app

featureFile = 'server.feature'
BASE_DIR = Path(__file__).resolve().parent.parent
FEATURE_FILE = BASE_DIR.joinpath('features').joinpath(featureFile).__str__()


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    # create the app with common test config
    app = create_app({"TESTING": True})

    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@scenario(FEATURE_FILE, 'server starts and passed health checks')
def test_server():
    print("End of server test")
    pass


print(FEATURE_FILE)


def pytest_configure():
    pytest.server = app
    pytest.response = ''


@given('server is running')
def running():
    print("running")


@when('querying the health endpoint')
def set_string_to_hello_world(client):
    pytest.response = client.get("/health")


@then('server responds with pong')
def string_equals_hello_world():
    assert pytest.response.data == b'pong'


@scenario(FEATURE_FILE, 'withdrawing 1$ returns 1$ coin')
def test_withdrawing_one_dollar():
    print("End of withdrawing 1$ test")
    pass


@given('atm is loaded with 1$ coin')
def load_one_dollar(client):
    pass


@when('withdrawing 1$')
def withdrawing_one_dollar(client):
    pass


@then('receiving 1$ coin')
def receiving_one_dollar():
    pass

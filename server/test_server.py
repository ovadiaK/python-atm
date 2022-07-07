from pytest_bdd import scenario, given, when, then
from pathlib import Path
import pytest

from server import start, endpoint, app

featureFile = 'server.feature'
BASE_DIR = Path(__file__).resolve().parent.parent
FEATURE_FILE = BASE_DIR.joinpath('features').joinpath(featureFile)

print(FEATURE_FILE)


def pytest_configure():
    pytest.server = app
    pytest.response = ''


@scenario(FEATURE_FILE.__str__(), 'server starts and passed health checks')
def test_server():
    print("End of server test")
    pass


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@given('server is running')
def running():
    print("running")


@when('querying the health endpoint')
def set_string_to_hello_world(client):
    pytest.response = client.get("/health")


@then('server responds with pong')
def string_equals_hello_world():
    assert pytest.response.data == b'pong'

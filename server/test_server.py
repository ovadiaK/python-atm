from pytest_bdd import scenario, given, when, then
from pathlib import Path
import pytest

from server import create_app

featureFile = 'server.feature'
BASE_DIR = Path(__file__).resolve().parent.parent
FEATURE_FILE = BASE_DIR.joinpath('features').joinpath(featureFile).__str__()


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        return client


@scenario(FEATURE_FILE, 'server starts and passed health checks')
def test_server():
    print("End of server test")
    pass


def pytest_configure():
    pytest.response = ''


@given('server is running')
def running():
    print("\nserver running\n")


@when('querying the health endpoint')
def query_health_endpoint(client):
    pytest.response = client.get("/health")


@then('server responds with pong')
def server_responds_pong():
    assert pytest.response.data == b'pong'


@scenario(FEATURE_FILE, 'withdrawing 1$ returns 1$ coin')
def test_withdrawing_one_dollar():
    print("End of withdrawing 1$ test")
    pass


@when('withdrawing 1$')
def withdrawing_one_dollar(client):
    withdraw_amount(client, 1)


def withdraw_amount(client, amount):
    rv = client.put("/withdraw")
    pytest.response = rv.get_json()


@then('receiving 1$ coin')
def receiving_one_dollar():
    assert pytest.response == {"result": {"bills": [{}], "coins": [{"1": 1}]}}


@scenario(FEATURE_FILE, 'withdrawing 20$ should return bills')
def test_return_20_dollar():
    print("End of withdrawing 20$ test")
    pass


@when('withdrawing 20$')
def withdrawing_20_dollar(client):
    withdraw_amount(client, 20)


@then('receiving 20$ bill')
def receiving_20_dollar_bill():
    assert pytest.response == {"result": {"bills": [{"20": 1}], "coins": [{}]}}

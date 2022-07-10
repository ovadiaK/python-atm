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
    pytest.json = ''


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
    rv = client.post("/withdrawal", json={"amount": amount})
    pytest.response = rv
    pytest.json = rv.get_json()


@then('receiving 1$ coin')
def receiving_one_dollar():
    assert pytest.json == {"result": {"bills": [{}], "coins": [{"1": 1}]}}


@scenario(FEATURE_FILE, 'withdrawing 20$ should return bills')
def test_return_20_dollar():
    print("End of withdrawing 20$ test")
    pass


@when('withdrawing 20$')
def withdrawing_20_dollar(client):
    withdraw_amount(client, 20)


@then('receiving 20$ bill')
def receiving_20_dollar_bill():
    assert pytest.json == {"result": {"bills": [{"20": 1}], "coins": [{}]}}


@scenario(FEATURE_FILE, 'withdrawing more money than loaded')
def test_more_than_max_amount(client):
    print("End of test more than allowed amount")
    pass


@given('is loaded with 1000$')
def withdraw_until_1000(client):
    withdraw_amount(client, 1216.41)


@when('withdrawing 1200$')
def withdrawing_1200(client):
    withdraw_amount(client, 1200)


@then('error 409 and max amount is returned')
def more_than_exists():
    assert pytest.response.status_code == 409
    assert pytest.json == {"maximum": 1000}


@scenario(FEATURE_FILE, 'withdrawing with too small decimal will be floored')
def test_too_small_decimal():
    print("too small decimal test passed")
    pass


@when('withdrawing 20.00001$')
def withdrawing_too_small(client):
    withdraw_amount(client, 20.00001)


@scenario(FEATURE_FILE, 'withdrawing is limited to 2000$')
def test_more_than_2000():
    print('withdrawing more than 2000 test passed')
    pass


@when('withdrawing 2200$')
def withdrawing_too_much(client):
    withdraw_amount(client, 3000)


@then('receiving only 2000$')
def receive_max():
    assert pytest.json == {'result': {'bills': [{'100': 4, '20': 10, '200': 7}], 'coins': [{}]}}


@scenario(FEATURE_FILE, 'too many coins will throw exception')
def test_too_many_coins():
    print('throwing too many coins exception passed')
    pass


@given('no bills left')
def withdraw_all_bills(client):
    withdraw_amount(client, 2000)
    withdraw_amount(client, 100)


@when('withdrawing all coins')
def withdraw_all_coins(client):
    withdraw_amount(client, 116.40)


@then('too many coins exception is thrown')
def too_many_coins_exception():
    assert pytest.response.status_code == 409
    assert pytest.json == {"error": "TooManyCoinsException"}

from pytest_bdd import scenario, given, when, then
from pathlib import Path
import pytest


featureFile = 'atm_server.feature'
BASE_DIR = Path(__file__).resolve().parent.parent
FEATURE_FILE = BASE_DIR.joinpath('features').joinpath(featureFile).__str__()


@scenario(FEATURE_FILE, 'server starts and passed health checks')
def test_server():
    print("End of atm_server test")
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


@scenario(FEATURE_FILE, 'refill api responds with status 200')
def test_refill_responds_ok():
    print('refill api responds with status 200 passed')
    pass


@scenario(FEATURE_FILE, 'refill api can refill the atm money')
def test_refill_20_dollar():
    print('refill api can refill the atm money passed')
    pass


@when('refilling 20$ bill')
def refilling_20_dollar(client):
    json_struct = {"bills": {"20": 1}, "coins": {}}
    refill_atm(client, json_struct)


def refill_atm(client, json_struct):
    rv = client.post("/refill", json=json_struct)
    pytest.response = rv
    pytest.json = rv.get_json()


@then('server responds with 200 status ok')
def status_ok():
    assert pytest.response.status_code == 200


refill_coins = 'refill empty atm with coins'


@scenario(FEATURE_FILE, refill_coins)
def test_refill_coins():
    print(refill_coins, "passed")
    pass


@given('atm has only change left')
def atm_empty(client):
    withdraw_all_bills(client)
    withdraw_amount(client, 115)


@when('refilling 4 5$ coins')
def refill_4_5_dollar_coins(client):
    json_struct = {"bills": {}, "coins": {"5": 4}}
    refill_atm(client, json_struct)


@then('receiving 4 5$ coins')
def got_4_5_dollar_coins():
    assert pytest.json == {"result": {"bills": [{}], "coins": [{"5": 4}]}}


invalid_bill = 'refill with invalid bill'


@scenario(FEATURE_FILE, invalid_bill)
def test_invalid_bill():
    print(invalid_bill, "passed")
    pass


@when('refilling 250$ bill')
def refill_invalid_bill(client):
    json_struct = {"bills": {"250": 1}, "coins": {}}
    refill_atm(client, json_struct)


@then('server responds with 400')
def client_error():
    assert pytest.response.status_code == 400


invalid_coin = 'refill with invalid coin'


@scenario(FEATURE_FILE, invalid_coin)
def test_invalid_coin():
    print(invalid_coin, "passed")
    pass


@when('refilling with 6$ coin')
def refill_invalid_coin(client):
    json_struct = {"bills": {}, "coins": {"6": 1}}
    refill_atm(client, json_struct)

from pytest_bdd import scenario, given, when, then
from pathlib import Path
import pytest

from server import start, endpoint

featureFile = 'server.feature'
BASE_DIR = Path(__file__).resolve().parent.parent
FEATURE_FILE = BASE_DIR.joinpath('features').joinpath(featureFile)

print(FEATURE_FILE)


def pytest_configure():
    pytest.response = ''


@scenario(FEATURE_FILE.__str__(), 'server starts and passed health checks')
def test_server_world():
    print("End of server test")
    pass


@given('server is running')
def empty_string():
    start()


@when('querying the health endpoint')
def set_string_to_hello_world():
    pytest.response = endpoint()


@then('server responds with status ok')
def string_equals_hello_world():
    assert pytest.response == "200"

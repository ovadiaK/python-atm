from pytest_bdd import scenario, given, when, then
from pathlib import Path
import pytest

featureFile = 'hello.feature'
BASE_DIR = Path(__file__).resolve().parent
FEATURE_FILE = BASE_DIR.joinpath(featureFile)


def pytest_configure():
    pytest.STRING = ''


@scenario(FEATURE_FILE, 'Printing hello world')
def test_hello_world():
    print("End of hello world test")
    pass


@given('there is an empty string')
def empty_string():
    pytest.String = ''


@when('the string is set to hello world')
def set_string_to_hello_world():
    pytest.String = 'hello world'


@then('the string is hello world')
def string_equals_hello_world():
    assert pytest.String == "hello world"

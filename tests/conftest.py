import pytest

from atm_server.server import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        return client

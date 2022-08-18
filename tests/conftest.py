import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app('default')
    app.config.update({
        "TESTING": True,
    })
    yield app

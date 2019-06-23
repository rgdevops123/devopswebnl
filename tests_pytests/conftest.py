from config import config_dict
from pytest import fixture
from app import create_app


@fixture
def base_client():
    app = create_app(config_dict['Test1'])
    app_ctx = app.app_context()
    app_ctx.push()
    yield app.test_client()

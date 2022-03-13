import pytest

from api.client import ApiClient


@pytest.fixture(scope='session')
def api_client() -> ApiClient:
    api_client = ApiClient(base_url="https://target.my.com/", email="nik-stepanov-2001@bk.ru",
                           password="autotests")
    return api_client

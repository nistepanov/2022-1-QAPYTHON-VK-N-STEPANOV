import pytest
import os

from mysql.client import MySqlClient


@pytest.fixture(scope='session')
def mysql_client_fixture():
    mysql_client = MySqlClient(user='root', password='pass', db_name='TEST_SQL')
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope='function')
def file_path(repo_root):
    return os.path.join(repo_root, 'resources', 'access.log')


def pytest_configure(config):
    mysql_client = MySqlClient(user='root', password='pass', db_name='TEST_SQL')
    mysql_client.drop_db()
    mysql_client.create_db()

import pytest

from mysql.builder import MySqlBuilder


class MySqLTest:

    def prepare(self, file_path):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client_fixture, file_path):
        self.mysql = mysql_client_fixture
        self.mysql_builder = MySqlBuilder(mysql_client_fixture)
        self.prepare(file_path)

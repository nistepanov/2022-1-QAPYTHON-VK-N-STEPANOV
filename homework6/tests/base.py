import pytest
from mysql.builder import MySqlBuilder


class MySqLTest:

    def prepare(self, file_path):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, file_path):
        self.mysql = mysql_client
        self.mysql_builder = MySqlBuilder(mysql_client)
        self.prepare(file_path)

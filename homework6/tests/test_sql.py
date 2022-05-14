import pytest

from mysql.utils.models import *
from parser_log.parser import *
from tests.base import MySqLTest


class TestCountRequests(MySqLTest):

    def prepare(self, path):
        self.mysql.create_table('count_requests')
        self.total_requests_from_parse = count_requests(self.mysql_builder, path)
        self.mysql.session.commit()

        self.count_parsed = 225132
        self.lines_from_db = self.mysql.session.query(CountRequests).first()

    @pytest.mark.SQL
    def test_count_total_number_of_request(self):
        assert self.count_parsed == self.lines_from_db.count


class TestCountRequestsType(MySqLTest):

    def prepare(self, path):
        self.mysql.create_table('count_requests_type')
        self.total_requests_by_type_from_parse = count_requests_type(self.mysql_builder, path)
        self.mysql.session.commit()

        self.count_parsed = len(self.total_requests_by_type_from_parse)
        self.lines_from_db = self.mysql.session.query(CountRequestsType).all()

        self.total_get_requests_from_db = self.mysql.session.query(CountRequestsType).filter_by(type="GET").first()

        self.total_post_requests_from_db = self.mysql.session.query(CountRequestsType).filter_by(type="POST").first()

        self.total_put_requests_from_db = self.mysql.session.query(CountRequestsType).filter_by(type="PUT").first()

        self.total_head_requests_from_db = self.mysql.session.query(CountRequestsType).filter_by(type="HEAD").first()

    @pytest.mark.SQL
    def test_count_total_requests_separate_by_type(self):
        assert len(self.lines_from_db) == self.count_parsed
        assert self.total_get_requests_from_db.count == self.total_requests_by_type_from_parse["GET"]
        assert self.total_post_requests_from_db.count == self.total_requests_by_type_from_parse["POST"]
        assert self.total_put_requests_from_db.count == self.total_requests_by_type_from_parse["PUT"]
        assert self.total_head_requests_from_db.count == self.total_requests_by_type_from_parse["HEAD"]


class TestCountTopResource(MySqLTest):
    count = 10

    @staticmethod
    def parse_resources_db(line_from_db):
        path = str(line_from_db).split('=')[2].split(',')[0]
        count = int(str(line_from_db).split('=')[3].replace("'", ''))
        return [path, count]

    def prepare(self, path):
        self.mysql.create_table('count_top_resources')
        self.top_resources = count_top_resource(self.mysql_builder, path, self.count)
        self.mysql.session.commit()

        self.lines = self.mysql.session.query(CountTopResources).all()

    @pytest.mark.SQL
    def test_top_requests_by_usage(self):
        assert len(self.lines) == self.count
        for i in range(0, len(self.lines)):
            resources = self.parse_resources_db(self.lines[i])
            assert resources[0].replace("'", '') == self.top_resources[i][0]
            assert resources[1] == self.top_resources[i][1]


class TestTopSizeRequestsClientError(MySqLTest):
    count = 5

    @staticmethod
    def parse_resources_db(line_from_db):
        path = str(line_from_db).split(':')[2].split(',')[0]
        ip = str(line_from_db).split(':')[3].split(',')[0].replace("'", '')
        size = int(str(line_from_db).split(':')[4].split(',')[0].replace("'", ''))
        code = int(str(line_from_db).split(':')[5].split(',')[0].replace("'", ''))
        return [path, ip, size, code]

    def prepare(self, path):
        self.mysql.create_table('count_requests_client_error')
        self.top_biggest_requests_cl_error = top_biggest_requests_ended_client_error(self.mysql_builder, path,
                                                                                     self.count)
        self.mysql.session.commit()

        self.lines = self.mysql.session.query(CountTopSizeRequestsClientError).all()

    @pytest.mark.SQL
    def test_top_five_biggest_requests_ended_client_error(self):
        assert len(self.lines) == self.count
        for i in range(0, len(self.lines)):
            resources = self.parse_resources_db(self.lines[i])
            assert resources[0].replace("'", '') == self.top_biggest_requests_cl_error[i][0].split(" ")[0]
            assert resources[1] == self.top_biggest_requests_cl_error[i][0].split(" ")[2]
            assert resources[2] == self.top_biggest_requests_cl_error[i][1]
            assert resources[3] == int(self.top_biggest_requests_cl_error[i][0].split(" ")[1])


class TestTopRequestsServerError(MySqLTest):
    count = 5

    @staticmethod
    def parse_resources_db(line_from_db):
        frequency = int(str(line_from_db).split(':')[2].split(',')[0].replace("'", ''))
        ip = str(line_from_db).split(':')[3].split(',')[0].replace("'", '')
        return [ip, frequency]

    def prepare(self, path):
        self.mysql.create_table('count_requests_server_error')
        self.top_biggest_requests_serv_error = top_requests_ended_server_error(self.mysql_builder, path, self.count)
        self.mysql.session.commit()

        self.lines = self.mysql.session.query(CountTopFrequencyRequestsServerError).all()

    @pytest.mark.SQL
    def test_top_five_requests_ended_server_error(self):
        assert len(self.lines) == self.count
        for i in range(0, len(self.lines)):
            resources = self.parse_resources_db(self.lines[i])
            assert resources[0] == self.top_biggest_requests_serv_error[i][0]
            assert resources[1] == self.top_biggest_requests_serv_error[i][1]

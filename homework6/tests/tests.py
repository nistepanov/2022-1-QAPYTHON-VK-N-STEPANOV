from mysql.models import *
from parser_log.parser import *
from .base import MySqLTest


class TestCountRequests(MySqLTest):
    count = 1

    def prepare(self, path):
        count_requests(self.mysql_builder, path)
        self.mysql.session.commit()

    def test_count_total_number_of_request(self):
        line = self.mysql.session.query(CountRequests).all()
        assert len(line) == self.count


class TestCountRequestsType(MySqLTest):
    count = 4

    def prepare(self, path):
        count_requests_type(self.mysql_builder, path)
        self.mysql.session.commit()

    def test_count_total_requests_separate_by_type(self):
        line = self.mysql.session.query(CountRequestsType).all()
        assert len(line) == self.count


class TestCountTopResource(MySqLTest):
    count = 10

    def prepare(self, path):
        count_top_resource(self.mysql_builder, path)
        self.mysql.session.commit()

    def test_top_ten_requests_by_usage(self):
        line = self.mysql.session.query(CountTopResources).all()
        assert len(line) == self.count


class TestBigRequestsError(MySqLTest):
    count = 5

    def prepare(self, path):
        top_five_biggest_requests_ended_client_error(self.mysql_builder, path)
        self.mysql.session.commit()

    def test_top_five_biggest_requests_ended_client_error(self):
        line = self.mysql.session.query(CountTopSizeRequestsClientError).all()
        assert len(line) == self.count


class TestInternalError(MySqLTest):
    count = 5

    def prepare(self, path):
        top_five_requests_ended_server_error(self.mysql_builder, path)
        self.mysql.session.commit()

    def test_top_five_requests_ended_server_error(self):
        line = self.mysql.session.query(CountTopFrequencyRequestsServerError).all()
        assert len(line) == self.count

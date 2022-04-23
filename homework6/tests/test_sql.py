import pytest

from mysql.utils.models import *
from parser_log.parser import *
from tests.base import MySqLTest


class TestCountRequests(MySqLTest):
    count = 1

    def prepare(self, path):
        self.mysql.create_count_requests()
        count_requests(self.mysql_builder, path)
        self.mysql.session.commit()

    @pytest.mark.SQL
    def test_count_total_number_of_request(self):
        line = self.mysql.session.query(CountRequests).all()

        assert len(line) == self.count


class TestCountRequestsType(MySqLTest):
    count = 4

    def prepare(self, path):
        self.mysql.create_count_requests_type()
        count_requests_type(self.mysql_builder, path)
        self.mysql.session.commit()

    @pytest.mark.SQL
    def test_count_total_requests_separate_by_type(self):
        line = self.mysql.session.query(CountRequestsType).all()

        assert len(line) == self.count


class TestCountTopResource(MySqLTest):
    count = 10

    def prepare(self, path):
        self.mysql.create_count_top_resources()
        count_top_resource(self.mysql_builder, path)
        self.mysql.session.commit()

    @pytest.mark.SQL
    def test_top_ten_requests_by_usage(self):
        line = self.mysql.session.query(CountTopResources).all()

        assert len(line) == self.count


class TestTopSizeRequestsClientError(MySqLTest):
    count = 5

    def prepare(self, path):
        self.mysql.create_client_error_requests()
        top_five_biggest_requests_ended_client_error(self.mysql_builder, path)
        self.mysql.session.commit()

    @pytest.mark.SQL
    def test_top_five_biggest_requests_ended_client_error(self):
        line = self.mysql.session.query(CountTopSizeRequestsClientError).all()

        assert len(line) == self.count


class TestTopRequestsServerError(MySqLTest):
    count = 5

    def prepare(self, path):
        self.mysql.create_server_errors_requests()
        top_five_requests_ended_server_error(self.mysql_builder, path)
        self.mysql.session.commit()

    @pytest.mark.SQL
    def test_top_five_requests_ended_server_error(self):

        line = self.mysql.session.query(CountTopFrequencyRequestsServerError).all()

        assert len(line) == self.count

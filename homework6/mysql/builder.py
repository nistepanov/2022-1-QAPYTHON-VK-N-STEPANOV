from mysql.utils.models import *


class MySqlBuilder:

    def __init__(self, client):
        self.client = client

    def create_count_requests(self, count):
        count_requests = CountRequests(count=count)
        self.client.session.add(count_requests)
        return count_requests

    def create_count_req_type(self, type, count):
        count_requests_separeted_by_type = CountRequestsType(
            type=type,
            count=count
        )
        self.client.session.add(count_requests_separeted_by_type)
        return count_requests_separeted_by_type

    def create_count_top_res(self, path, count):
        top_ten_requests = CountTopResources(
            path=path,
            count=count
        )
        self.client.session.add(top_ten_requests)
        return top_ten_requests

    def create_count_req_client_error(self, path, code, ip, size):
        top_five_requests = CountTopSizeRequestsClientError(
            path=path,
            code=code,
            ip=ip,
            size=size
        )
        self.client.session.add(top_five_requests)
        return top_five_requests

    def create_count_req_server_error(self, ip, frequency):
        top_five_requests = CountTopFrequencyRequestsServerError(
            ip=ip,
            frequency=frequency
        )
        self.client.session.add(top_five_requests)
        return top_five_requests

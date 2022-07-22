import ast

import pytest


class BaseApi:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        if not self.api_client.session.cookies:
            self.api_client.set_all_necessary_cookies()
        else:
            pass

    def create_campaign(self, name):
        json_data = {
            'name': name,
            'objective': 'traffic',
            'package_id': 961,
        }

        additional_headers_for_campaign = {'Host': 'target.my.com', 'Referer':
            'https://target.my.com/campaign/new'}

        headers = {**self.api_client.session.headers, **additional_headers_for_campaign}

        return self.api_client._request(method='POST', location='api_myapp/v2/campaigns.json', json=json_data,
                                        headers=headers)

    def check_campaign_is_created(self, id_campaign, name):
        params = {'fields': 'id, name, status',
                  'sorting': '-id',
                  'status': 'active'}

        response = self.api_client._request(method='GET', location='api_myapp/v2/campaigns.json', params=params)

        response_as_dict = ast.literal_eval(response.text)
        recently_created_campaign = response_as_dict['items'][0]

        try:
            assert recently_created_campaign["id"] == id_campaign, "Ids of campaigns are not equal!"
        except AssertionError:
            return False

        try:
            assert recently_created_campaign["name"] == name, "Names of campaigns are not equal!"
        except AssertionError:
            return False
        else:
            return True

    def delete_campaign(self, id_campaign):
        json_data = [{"id": id_campaign,
                      "status": "deleted"}]

        self.api_client._request(method='POST', location='api_myapp/v2/campaigns/mass_action.json', json=json_data,
                                 expected_status=204)

    def check_campaign_is_deleted(self, id_campaign, name):
        params = {'fields': 'id, name, status',
                  'sorting': '-id',
                  'status': 'deleted'}

        response = self.api_client._request(method='GET', location='api_myapp/v2/campaigns.json', params=params)

        response_as_dict = ast.literal_eval(response.text)

        try:
            recently_deleted_campaign = response_as_dict['items'][0]
            if recently_deleted_campaign["id"] == id_campaign and recently_deleted_campaign["name"] == name:
                return True

        except:
            return False

        return False

    def create_segment(self, name):
        json_data = {"name": name, "pass_condition": 1, "relations": [
            {"object_type": "remarketing_player", "params": {"type": "positive", "left": 365, "right": 0}}]}

        response = self.api_client._request(method="POST", location="api_myapp/v2/remarketing/segments.json",
                                            json=json_data)

        return response

    def check_segment_is_created(self, id_segment, name):
        params = {'sorting': '-id'}
        response = self.api_client._request(method="GET", location="api_myapp/v2/remarketing/segments.json",
                                            params=params)
        response_as_dict = ast.literal_eval(response.text)

        try:
            recently_created_segment = response_as_dict['items'][0]
            if recently_created_segment["id"] == id_segment and recently_created_segment["name"] == name:
                return True

        except:
            return False

        return False

    def check_segment_is_deleted(self, id_segment, name):

        response = self.api_client._request(method='GET', location='api_myapp/v2/campaigns.json')

        response_as_dict = ast.literal_eval(response.text)

        for items in response_as_dict['items']:
            if items["id"] == id_segment and items["name"] == name:
                return False

        return True

    def delete_segment(self, id_segment):
        json_data = [{"source_id": id_segment, "source_type": "segment"}]

        self.api_client._request(method="POST", location="api_myapp/v1/remarketing/mass_action/delete.json", json=json_data)

from urllib.parse import urljoin

import requests
from requests.utils import dict_from_cookiejar
from requests.cookies import cookiejar_from_dict


class InvalidLoginException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.session = requests.Session()

    def _request(self, method, location, headers=None, data=None, expected_status=200, params=None,
                 cookies=None, json=None):
        if "http" in location:
            url = location
        else:
            url = urljoin(self.base_url, location)

        if cookies is not None:
            response = self.session.request(method=method, url=url, headers=headers, data=data, params=params,
                                            cookies=cookies, json=json)
        else:
            response = self.session.request(method=method, url=url, headers=headers, data=data, params=params,
                                            json=json)

        try:
            assert response.status_code == expected_status

        except AssertionError:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"'
                                              f'\nExpected {expected_status} for URL {url}')

        return response

    def auth_login(self):
        auth_login = 'https://auth-ac.my.com/auth'

        self.session.headers = {
            'Connection': 'keep-alive',
            'Origin': 'https://target.my.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/100.0.4896.60 Safari/537.36',
        }

        params = {
            'lang': 'ru',
            'nosavelogin': '0',
        }

        data = {
            'email': self.email,
            'password': self.password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/',
        }

        referer_headers = {'Referer': 'https://target.my.com/'}
        headers = {**self.session.headers, **referer_headers}

        response = self._request(method="POST", location=auth_login, headers=headers, params=params,
                                 data=data)

        try:
            z = dict_from_cookiejar(response.cookies)['z']
            mrcu = dict_from_cookiejar(response.history[0].cookies)['mrcu']
            sdc = dict_from_cookiejar(response.history[5].history[3].cookies)['sdc']
            mc = dict_from_cookiejar(response.history[2].history[1].cookies)['mc']

        except KeyError:
            raise InvalidLoginException("Authorisation Error! Invalid login or password!")

        cookies = {'mc': mc, 'mrcu': mrcu, 'sdc': sdc, 'z': z}

        return cookies

    def set_all_necessary_cookies(self):
        get_csrf_token_url = 'https://target.my.com/csrf/'
        cookies_auth = self.auth_login()
        response = self._request(method="GET", location=get_csrf_token_url, cookies=cookiejar_from_dict(cookies_auth))

        crsftoken_value = dict_from_cookiejar(response.cookies)['csrftoken']
        csrftoken = {'csrftoken': crsftoken_value}

        self.session.headers['X-CSRFToken'] = crsftoken_value
        all_necessary_cookies = cookies_auth | csrftoken

        self.session.cookies = cookiejar_from_dict(all_necessary_cookies)

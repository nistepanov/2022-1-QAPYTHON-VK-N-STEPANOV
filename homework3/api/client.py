from urllib.parse import urljoin

import requests
from requests.utils import dict_from_cookiejar
from requests.cookies import cookiejar_from_dict

from .Exceptions import InvalidLoginException, ResponseStatusCodeException


class ApiClient:

    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.session = requests.Session()

    def _request(self, method, location, headers=None, data=None, expected_status=200, params=None, json=None,
                 allow_redirects=False):
        if "http" in location:
            url = location
        else:
            url = urljoin(self.base_url, location)

        response = self.session.request(method=method, url=url, headers=headers, data=data, params=params, json=json,
                                        allow_redirects=allow_redirects, cookies=self.session.cookies)
        try:
            assert response.status_code == expected_status

        except AssertionError:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"'
                                              f'\nExpected {expected_status} for URL {url}')

        return response

    def auth_login_cookies(self):
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

        self.session.headers['Referer'] = 'https://target.my.com/'

        self._request(method="POST", location=auth_login, headers=self.session.headers, params=params,
                      data=data, allow_redirects=True)

    def crsf_token_cookies(self):
        get_csrf_token_url = 'https://target.my.com/csrf/'
        response = self._request(method="GET", location=get_csrf_token_url)

        crsftoken_value = dict_from_cookiejar(response.cookies)['csrftoken']

        self.session.headers['X-CSRFToken'] = crsftoken_value

    def set_all_necessary_cookies(self):
        self.auth_login_cookies()
        self.crsf_token_cookies()

        try:
            z = self.session.cookies['z']
            mrcu = self.session.cookies['mrcu']
            sdc = self.session.cookies['sdc']
            mc = self.session.cookies['mc']
            csrftoken = self.session.cookies['csrftoken']

        except KeyError:
            raise InvalidLoginException("Authorisation Error! Invalid login or password!")

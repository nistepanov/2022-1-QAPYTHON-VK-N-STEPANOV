from urllib.parse import urljoin

import allure
import requests

from final_project.code.settings.config import *


class ApiClient:

    @allure.step("Выполняем инициализацию API-client'a")
    def __init__(self):
        self.url = f"http://{APP_HOST}:{APP_PORT}"
        # self.url = f"http://127.0.0.1:8086"
        self.session = requests.Session()

    @allure.step("Авторизуемся по стабильным данным - выполянем POST запрос /login")
    def auth_login_cookies(self, data=None):
        self.session.headers = {
        }

        if data is None:
            data = {
                'username': "nikita",
                'password': "test",
            }

        return self._request(method="POST", location="/login", headers=self.session.headers,
                             data=data)

    @allure.step("Выполняем запрос")
    def _request(self, method, location, headers=None, data=None, params=None, json=None, url=None,
                 allow_redirects=False):
        if location and url is None:
            url = urljoin(self.url, location)
        elif location and url is not None:
            url = urljoin(url, location)
        else:
            url = self.url
        response = self.session.request(method=method, url=url, headers=headers, data=data,
                                        params=params, json=json, allow_redirects=allow_redirects,
                                        cookies=self.session.cookies)

        return response

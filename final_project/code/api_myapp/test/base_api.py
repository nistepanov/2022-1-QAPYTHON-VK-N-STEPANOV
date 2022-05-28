import allure
import pytest

from api_client import ApiClient
from final_project.server_mock.vk_api_mock import VK_API_HOST, VK_API_PORT

vk_mock_url = f"http://vk_api:{VK_API_PORT}"


class BaseApi:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client_fixture):
        with allure.step("Выполняем коннект к БД и возвращаем объект соединения"):
            self.mysql = mysql_client_fixture
        self.api_client = ApiClient()
        if not self.api_client.session.cookies:
            self.api_client.auth_login_cookies()
        else:
            pass

    @allure.step("Выполняем POST запрос '/api/user'")
    def post_create_user(self, complex_data):
        headers = {**{"Content-Type": "application/json"}, **self.api_client.session.headers}
        response = self.api_client._request(method="POST", location="/api/user",
                                            headers=headers,
                                            json=complex_data)

        return response

    @allure.step("Выполняем DELETE запрос '/api/user/{username}'")
    def delete_user(self, username):
        response = self.api_client._request(method="DELETE", location=f"/api/user/{username}")

        return response

    @allure.step("Выполняем PUT запрос '/api/user/{username}/change-password'")
    def put_change_password(self, username, new_password):
        response = self.api_client._request(method="PUT", location=f"/api/user/{username}/change-password",
                                            json={"password": new_password})

        return response

    @allure.step("Выполняем POST запрос '/api/user/{username}/block'")
    def post_block_user(self, username):
        response = self.api_client._request(method="POST", location=f"/api/user/{username}/block")
        return response

    @allure.step("Выполняем POST запрос '/api/user/{username}/accept'")
    def post_unblock_user(self, username):
        response = self.api_client._request(method="POST", location=f"/api/user/{username}/accept")

        return response

    @allure.step("Выполняем GET запрос '/status'")
    def get_status(self):
        response = self.api_client._request(method="GET", location="/status")

        return response

    @allure.step("Выполняем GET запрос 'http://<VK_URL>/vk_id/<username>'")
    def get_vk_id_from_mock(self, username):
        response = self.api_client._request(method="GET", location=f"/vk_id/{username}", url=vk_mock_url)

        return response

    @allure.step("Выполняем GET запрос '/logout'")
    def get_logout(self):
        response = self.api_client._request(method="GET", location="/logout")

        return response

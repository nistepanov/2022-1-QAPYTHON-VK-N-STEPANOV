import json
import re

import allure
import pytest

from requests.utils import dict_from_cookiejar

from base_api import BaseApi
from final_project.code.mysql.utils.models import Users
from final_project.code.tools.create_user_info import UserInfo
from final_project.code.tools.randomizer import RandomGenerate


class TestApiAuthorizedUser(BaseApi):
    @allure.title("Создание пользовательских данных (без middle-name)")
    @pytest.fixture(scope='function')
    def create_user_data_without_middle_name(self):
        user_info = UserInfo()
        user_data = user_info.create_user_data()
        human_data = user_info.create_human_data()
        complex_data = {**user_data, **human_data}
        return complex_data

    @allure.title("Создание пользовательских данных (c middle-name)")
    @pytest.fixture(scope='function')
    def create_user_data_with_middle_name(self):
        user_info = UserInfo()
        user_data = user_info.create_user_data()
        human_data = user_info.create_human_data(option_middle_name=1)
        complex_data = {**user_data, **human_data}
        return complex_data

    @allure.title("Проверка создания пользователя без middle-name")
    @pytest.mark.API
    def test_post_create_user_without_middle_name_bug(self, create_user_data_without_middle_name):
        """
         Тестирование: Добавление пользователя (без middle-name)
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных
         Шаги:
         1. Отправка запроса по API
         2. Найти пользователя по email в БД
         3. Удалить из БД раннее созданного пользователя
         Ожидаемый результат:
         Пользователь добавляется в БД с корректными данными (+)
         Код ответа - 201 ("Created") (-)
         Фактический результат:
         Пользователь добавляется в БД с корректными данными
         Код ответа - 210
         """
        complex_user_data = create_user_data_without_middle_name
        self.mysql.session.commit()
        response = self.post_create_user(complex_user_data)
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        self.delete_user(complex_user_data["username"])

        assert user_db.username == complex_user_data['username'], f"Никнеймы не совпадают: В БД {user_db.username}; " \
                                                                  f"Отправлено в request body " \
                                                                  f"{complex_user_data['username']}"
        assert user_db.password == complex_user_data['password'], f"Пароли не совпадают: В БД {user_db.password}; " \
                                                                  f"Отправлено в request body " \
                                                                  f"{complex_user_data['password']}"
        assert user_db.email == complex_user_data['email'], f"Почтовые адреса не совпадают: В БД {user_db.email}; " \
                                                            f"Отправлено в request body " \
                                                            f"{complex_user_data['email']}"
        assert user_db.name == complex_user_data['name'], f"Имена не совпадают: В БД {user_db.name}; " \
                                                          f"Отправлено в request body " \
                                                          f"{complex_user_data['name']}"
        assert user_db.surname == complex_user_data['surname'], f"Фамилии не совпадают: В БД {user_db.surname}; " \
                                                                f"Отправлено в request body " \
                                                                f"{complex_user_data['surname']}"

        assert user_db.middle_name is None
        assert user_db.access == 1, "Access по умолчанию должен быть равен 1!"
        assert user_db.active == 0, "Active по умолчанию должен быть равен 0!"
        assert json.loads(response.text) == {
            "detail": "User was added",
            "status": "success"
        }, "Тело ответа приложения не соотв. ожидаемому"
        assert response.status_code == 201, "Код ответа приложения должен быть 201"

    @allure.title("Проверка создания пользователя с middle-name")
    @pytest.mark.API
    def test_post_create_user_with_middle_name_bug(self, create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя (c middle-name)
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных
         Шаги:
         1. Отправка запроса по API
         2. Найти пользователя по email в БД
         3. Удалить из БД ранее созданного пользователя
         Ожидаемый результат:
         Пользователь добавляется в БД с корректными данными (+)
         Код ответа - 201 ("Created") (-)
         Фактический результат:
         Пользователь добавляется в БД с корректными данными
         Код ответа - 210
         """
        complex_user_data = create_user_data_with_middle_name
        response = self.post_create_user(complex_user_data)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        self.delete_user(complex_user_data["username"])

        assert user_db.username == complex_user_data['username'], f"Никнеймы не совпадают: В БД {user_db.username}; " \
                                                                  f"Отправлено в request body " \
                                                                  f"{complex_user_data['username']}"
        assert user_db.password == complex_user_data['password'], f"Пароли не совпадают: В БД {user_db.password}; " \
                                                                  f"Отправлено в request body " \
                                                                  f"{complex_user_data['password']}"
        assert user_db.email == complex_user_data['email'], f"Почтовые адреса не совпадают: В БД {user_db.email}; " \
                                                            f"Отправлено в request body " \
                                                            f"{complex_user_data['email']}"
        assert user_db.name == complex_user_data['name'], f"Имена не совпадают: В БД {user_db.name}; " \
                                                          f"Отправлено в request body " \
                                                          f"{complex_user_data['name']}"
        assert user_db.surname == complex_user_data['surname'], f"Фамилии не совпадают: В БД {user_db.surname}; " \
                                                                f"Отправлено в request body " \
                                                                f"{complex_user_data['surname']}"

        assert user_db.middle_name == complex_user_data['middle_name'], f"Отчества не совпадают: В БД" \
                                                                        f" {user_db.middle_name}; " \
                                                                        f"Отправлено в request body " \
                                                                        f"{complex_user_data['middle_name']}"
        assert user_db.access == 1, "Access по умолчанию должен быть равен 1!"
        assert user_db.active == 0, "Active по умолчанию должен быть равен 0!"
        assert json.loads(response.text) == {
            "detail": "User was added",
            "status": "success"
        }, "Тело ответа приложения не соотв. ожидаемому"
        assert response.status_code == 201, "Код ответа приложения должен быть 201"

    @allure.title("Проверка создания пользователя без name")
    @pytest.mark.API
    def test_post_create_user_without_required_data_name(self, create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя (без name)
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных, удаление из пользов. данных поля name
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (+)
         Пользователь НЕ добавляется в БД (+)
         Фактический результат:
         Код ответа - 400 ("BAD REQUEST")
         Пользователь НЕ добавляется в БД
         """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data.pop('name')
        response = self.post_create_user(complex_user_data)

        assert json.loads(response.text) == {
            "detail": "Not exists required field ('name')",
            "status": "failed"
        }, "Тело ответа приложения не соотв. ожидаемому"
        assert response.status_code == 400, "Код ответа приложения должен быть 400"

    @allure.title("Проверка создания пользователя без surname")
    @pytest.mark.API
    def test_post_create_user_without_required_data_surname(self, create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя (без surname)
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных, удаление из пользов. данных поля surname
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (+)
         Пользователь НЕ добавляется в БД (+)
         Фактический результат:
         Код ответа - 400 ("BAD REQUEST")
         Пользователь НЕ добавляется в БД
         """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data.pop('surname')
        response = self.post_create_user(complex_user_data)

        assert json.loads(response.text) == {
            "detail": "Not exists required field ('surname')",
            "status": "failed"
        }, "Тело ответа приложения не соотв. ожидаемому"
        assert response.status_code == 400, "Код ответа приложения должен быть 400"

    @allure.title("Проверка создания пользователя без username")
    @pytest.mark.API
    def test_post_create_user_without_required_data_username(self, create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя (без username)
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных, удаление из пользов. данных поля username
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (+)
         Пользователь НЕ добавляется в БД (+)
         Фактический результат:
         Код ответа - 400 ("BAD REQUEST")
         Пользователь НЕ добавляется в БД
         """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data.pop('username')
        response = self.post_create_user(complex_user_data)

        assert json.loads(response.text) == {
            "detail": "Not exists required field ('username')",
            "status": "failed"
        }, "Тело ответа приложения не соотв. ожидаемому"
        assert response.status_code == 400, "Код ответа приложения должен быть 400"

    @allure.title("Проверка создания пользователя без email")
    @pytest.mark.API
    def test_post_create_user_without_required_data_email(self, create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя (без email)
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных, удаление из пользов. данных поля email
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (+)
         Пользователь НЕ добавляется в БД (+)
         Фактический результат:
         Код ответа - 400 ("BAD REQUEST")
         Пользователь НЕ добавляется в БД
         """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data.pop('email')
        response = self.post_create_user(complex_user_data)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['username']).first()

        assert user_db is None, "Пользователь не должен добавляться в БД"
        assert json.loads(response.text) == {
            "detail": "Not exists required field ('email')",
            "status": "failed"
        }, "Тело ответа приложения не соотв. ожидаемому"
        assert response.status_code == 400, "Код ответа приложения должен быть 400"

    @allure.title("Проверка создания пользователя без password")
    @pytest.mark.API
    def test_post_create_user_without_required_data_password(self, create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя (без password)
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных, удаление из пользов. данных поля password
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (+)
         Пользователь НЕ добавляется в БД (+)
         Фактический результат:
         Код ответа - 400 ("BAD REQUEST")
         Пользователь НЕ добавляется в БД
         """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data.pop('password')
        response = self.post_create_user(complex_user_data)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['username']).first()

        assert user_db is None, "Пользователь не должен добавляться в БД"
        assert json.loads(response.text) == {
            "detail": "Not exists required field ('password')",
            "status": "failed"
        }, "Тело ответа приложения не соотв. ожидаемому"
        assert response.status_code == 400, "Код ответа приложения должен быть 400"

    @allure.title("Проверка создания пользователя по email, который уже есть в БД")
    @pytest.mark.API
    def test_post_create_user_duplicate_data_email_bug(self, create_user_data_with_middle_name,
                                                       create_user_data_without_middle_name):
        """
         Тестирование: Добавление пользователя с данными, которые уже есть в БД (email)
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Пользователь НЕ добавляется в БД (+)
         Код ответа - 400 ("BAD REQUEST") (-)
         Фактический результат:
         Код ответа - 500 ("INTERNAL SERVER ERROR")
         Пользователь НЕ добавляется в БД
         """
        complex_user_data_first = create_user_data_with_middle_name
        email_first_user = complex_user_data_first["email"]

        self.post_create_user(complex_user_data_first)
        complex_user_data_second = create_user_data_without_middle_name
        complex_user_data_second["middle_name"] = create_user_data_with_middle_name["middle_name"]
        complex_user_data_second["email"] = email_first_user
        complex_user_data_second["username"] = RandomGenerate.generate_random_user_name()

        response = self.post_create_user(complex_user_data_second)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data_second['username']).first()

        assert user_db is None, "Пользователь не должен добавляться в БД"
        assert response.status_code == 400, "Код ответа приложения должен быть 400"
        assert json.loads(response.text) == {
            "detail": "User already exists",
            "status": "failed"
        }, "Тело ответа приложения не соотв. ожидаемому"

    @allure.title("Проверка создания пользователя по username, который уже есть в БД")
    @pytest.mark.API
    def test_post_create_user_duplicate_data_username(self, create_user_data_with_middle_name,
                                                      create_user_data_without_middle_name):
        """
         Тестирование: Добавление пользователя с данными, которые уже есть в БД (username)
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (+)
         Пользователь НЕ добавляется в БД (+)
         Фактический результат:
         Код ответа - 400 ("BAD REQUEST")
         Пользователь НЕ добавляется в БД
         """
        complex_user_data_first = create_user_data_with_middle_name
        username_first_user = complex_user_data_first["username"]

        self.post_create_user(complex_user_data_first)
        complex_user_data_second = create_user_data_without_middle_name
        complex_user_data_second["middle_name"] = create_user_data_with_middle_name["middle_name"]
        complex_user_data_second["username"] = username_first_user
        complex_user_data_second["email"] = RandomGenerate.generate_random_email()
        response = self.post_create_user(complex_user_data_second)

        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data_second['email']).first()

        assert user_db is None, "Пользователь не должен добавляться в БД"
        assert response.status_code == 400, "Код ответа приложения должен быть 400"
        assert json.loads(response.text) == {
            "detail": "User already exists",
            "status": "failed"
        }, "Тело ответа приложения не соотв. ожидаемому"

    @allure.title("Проверка создания пользователя по username, длина которого меньше допустимого (< 6 символов)")
    @pytest.mark.API
    def test_post_create_user_invalid_data_username_length_less_than_acceptable_bug(self,
                                                                                    create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя с неккоректными данными
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных, заменить username на слово, длиной меньше
         допустимого (меньше чем 6 символов)
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (-)
         Пользователь НЕ добавляется в БД (-)
         Фактический результат:
         Код ответа - 210 ("UNKNOWN")
         Пользователь добавляется в БД
         """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data["username"] = RandomGenerate.generate_random_user_name(1, 5)

        response = self.post_create_user(complex_user_data)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        assert response.status_code == 400, "Код ответа приложения должен быть 400"
        assert user_db is None, "Пользователь не должен добавляться в БД при невалидной длине username"

    @allure.title("Проверка создания пользователя по username, длина которого больше допустимого (> 16 символов)")
    @pytest.mark.API
    def test_post_create_user_invalid_data_username_length_more_than_acceptable_bug(self,
                                                                                    create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя с неккоректными данными
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных, заменить username на слово, длиной больше
         допустимого (больше чем 16 символов)
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (-)
         Пользователь НЕ добавляется в БД (+)
         Фактический результат:
         Код ответа - 500 ("INTERNAL SERVER ERROR")
         Пользователь НЕ добавляется в БД
         """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data["username"] = RandomGenerate.generate_random_user_name(17, 70)

        response = self.post_create_user(complex_user_data)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        assert response.status_code == 400, "Код ответа приложения должен быть 400"
        assert user_db is None, "Пользователь не должен добавляться в БД "

    @allure.title("Проверка создания пользователя по email, длина которого больше допустимого (> 64 символов)")
    @pytest.mark.API
    def test_post_create_user_invalid_data_email_length_more_than_acceptable_bug(self,
                                                                                 create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя с неккоректными данными
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных, заменить email на email, длиной больше
         допустимого (больше чем 64 символов)
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (-)
         Пользователь НЕ добавляется в БД (+)
         Фактический результат:
         Код ответа - 500 ("INTERNAL SERVER ERROR")
         Пользователь НЕ добавляется в БД
         """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data["email"] = RandomGenerate.generate_random_email(65, 70)

        response = self.post_create_user(complex_user_data)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        assert response.status_code == 400, "Код ответа приложения должен быть 400"
        assert user_db is None, "Пользователь не должен добавляться в БД "

    @allure.title("Проверка создания пользователя по password, длина которого больше допустимого (> 255 символов)")
    @pytest.mark.API
    def test_post_create_user_invalid_data_password_length_more_than_acceptable_bug(self,
                                                                                    create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя с неккоректными данными
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных, заменить password на password, длиной больше
         допустимого (больше чем 255 символов)
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (-)
         Пользователь НЕ добавляется в БД (+)
         Фактический результат:
         Код ответа - 500 ("INTERNAL SERVER ERROR")
         Пользователь НЕ добавляется в БД
         """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data["password"] = RandomGenerate.generate_random_password(256, 300)

        response = self.post_create_user(complex_user_data)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        assert response.status_code == 400, "Код ответа приложения должен быть 400"
        assert user_db is None, "Пользователь не должен добавляться в БД "

    @allure.title("Проверка создания пользователя по name, длина которого больше допустимого (> 255 символов)")
    @pytest.mark.API
    def test_post_create_user_invalid_data_name_length_more_than_acceptable_bug(self,
                                                                                create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя с неккоректными данными
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных, заменить name на name, длиной больше
         допустимого (больше чем 255 символов)
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (-)
         Пользователь НЕ добавляется в БД (+)
         Фактический результат:
         Код ответа - 500 ("INTERNAL SERVER ERROR")
         Пользователь НЕ добавляется в БД
         """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data["name"] = RandomGenerate.generate_random_user_name(256, 300)

        response = self.post_create_user(complex_user_data)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        assert response.status_code == 400, "Код ответа приложения должен быть 400"
        assert user_db is None, "Пользователь не должен добавляться в БД "

    @allure.title("Проверка создания пользователя по surname, длина которого больше допустимого (> 255 символов)")
    @pytest.mark.API
    def test_post_create_user_invalid_data_surname_length_more_than_acceptable_bug(self,
                                                                                   create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя с неккоректными данными
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных, заменить surname на surname, длиной больше
         допустимого (больше чем 255 символов)
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (-)
         Пользователь НЕ добавляется в БД (+)
         Фактический результат:
         Код ответа - 500 ("INTERNAL SERVER ERROR")
         Пользователь НЕ добавляется в БД
         """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data["surname"] = RandomGenerate.generate_random_user_name(256, 300)

        response = self.post_create_user(complex_user_data)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        assert response.status_code == 400, "Код ответа приложения должен быть 400"
        assert user_db is None, "Пользователь не должен добавляться в БД "

    @allure.title("Проверка создания пользователя по email, который не соотв. схеме имя@домен")
    @pytest.mark.API
    def test_post_create_user_invalid_email_schema_validation_bug(self, create_user_data_with_middle_name):
        """
         Тестирование: Добавление пользователя с неккоректными данными
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Авторизация, создание пользовательских данных, заменить email на email, который не соотв. схеме
         имя@домен
         Шаги:
         1. Отправка запроса по API
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (-)
         Пользователь НЕ добавляется в БД (+)
         Фактический результат:
         Код ответа - 210
         Пользователь добавляется в БД
         """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data["email"] = RandomGenerate.generate_random_password(10, 30)

        response = self.post_create_user(complex_user_data)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        assert response.status_code == 400, "Код ответа приложения должен быть 400"
        assert user_db is None, "Пользователь не должен добавляться в БД "

    @allure.title("Удаление пользователя")
    @pytest.mark.API
    def test_delete_user(self, create_user_data_with_middle_name):
        """
         Тестирование: Удаление пользователя
         Эндпоинт: DELETE http://127.0.0.1:8086/api/user/{username}
         Предусловия: Авторизация, создание пользовательских данных
         Шаги:
         1. Отправка запроса по API для создания пользователя - POST http://127.0.0.1:8086/api/user/
         2. Отправка запроса по API для удаления пользователя - DELETE http://127.0.0.1:8086/api/user/{name}
         Ожидаемый результат:
         Код ответа - 204 ("NO CONTENT") (-)
         Пользователь удаляется из БД (+)
         Фактический результат:
         Код ответа - 204 ("NO CONTENT")
         Пользователь удаляется из БД
         """
        complex_user_data = create_user_data_with_middle_name
        self.post_create_user(complex_user_data)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(username=complex_user_data['username']).first()

        assert user_db.username == complex_user_data['username'], f"Никнеймы не совпадают: В БД {user_db.username}; " \
                                                                  f"Отправлено в request body " \
                                                                  f"{complex_user_data['username']}"

        response = self.delete_user(complex_user_data["username"])
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(username=complex_user_data["username"]).first()

        assert user_db is None, "Пользователь должен быть удален!"
        assert response.status_code == 204, "Код ответа приложения должен быть 204"

    @allure.title("Смена пароля")
    @pytest.mark.API
    def test_put_change_password(self, create_user_data_with_middle_name):
        """
         Тестирование: Смена пароля
         Эндпоинт: PUT http://127.0.0.1:8086/api/user/{username}/change-password
         Предусловия: Авторизация, создание пользовательских данных
         Шаги:
         1. Отправка запроса по API для создания пользователя - POST http://127.0.0.1:8086/api/user/
         2. Сгенерировать новый пароль
         3. Отправка запроса по API для смены пароля пользователя - PUT http://127.0.0.1:8086/api/user/{
         name}/change-password (использовать новый пароль)
         4. Вернуть пароль в прежнее состояние
         Ожидаемый результат:
         Код ответа - 204 ("NO CONTENT") (+)
         Пароль пользователя изменяется корректно (меняется на переданный) (+)
         Фактический результат:
         Код ответа - 204 ("NO CONTENT")
         Пароль пользователя изменяется корректно (меняется на переданный)
         """
        complex_user_data = create_user_data_with_middle_name
        self.post_create_user(complex_user_data)
        self.mysql.session.commit()

        original_password = complex_user_data["password"]
        new_password = RandomGenerate.generate_random_password()

        response = self.put_change_password(complex_user_data['username'], new_password)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(username=complex_user_data["username"]).first()

        assert user_db.password == new_password, "Пароль должен быть изменен и равен новому паролю!"
        assert user_db.password != original_password, "Пароль должен быть изменен и не равен старому паролю!"
        assert response.status_code == 204, "Код ответа приложения должен быть 204"

        self.put_change_password(complex_user_data['username'], original_password)  # возвращаем пароль в
        # изначальное состояние

    @allure.title("Смена пароля на уже существующий в БД")
    @pytest.mark.API
    def test_put_change_password_on_already_exist_password(self, create_user_data_with_middle_name):
        """
         Тестирование: Смена пароля
         Эндпоинт: PUT http://127.0.0.1:8086/api/user/{username}/change-password
         Предусловия: Авторизация, создание пользовательских данных
         Шаги:
         1. Отправка запроса по API для создания пользователя - POST http://127.0.0.1:8086/api/user/
         2. Сохранить старый пароль
         3. Отправка запроса по API для смены пароля пользователя - PUT http://127.0.0.1:8086/api/user/{
         name}/change-password - использовать старый пароль
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (+)
         Информативное сообщение о том, что данный пароль уже используется кем-либо (+)
         Фактический результат:
         Код ответа - 400 ("BAD REQUEST")
         Информативное сообщение о том, что данный пароль уже используется кем-либо
         """
        complex_user_data = create_user_data_with_middle_name
        self.post_create_user(complex_user_data)
        self.mysql.session.commit()
        user_db = self.mysql.session.query(Users).filter_by(username=complex_user_data['username']).first()

        original_password_from_db = user_db.password

        response = self.put_change_password(complex_user_data['username'], original_password_from_db)

        assert response.status_code == 400, "Код ответа приложения должен быть 400"
        assert json.loads(response.text) == {
            "detail": "This password is already in use",
            "status": "failed"
        }, "Тело ответа приложения не соотв. ожидаемому"

    @allure.title("Блокировка пользователя")
    @pytest.mark.API
    def test_post_block(self):
        """
         Тестирование: Блокировка пользователя
         Эндпоинт: POST http://127.0.0.1:8086/api/user/{username}/block
         Предусловия: Авторизация, вытащить пользователя из БД с access == 1
         Шаги:
         1. Вытащить из БД значение username, access для любого пользователя
         2. Отправка запроса по API для смены флага доступа (блокировки пользователя) - POST
         http://127.0.0.1:8086/api/user/{username}/block
         3. Вернуть флаг access в изначальное состояние (разблокировать пользователя)
         Ожидаемый результат:
         Код ответа - 200 ("OK") (+)
         Флаг доступа пользователя access меняется с 1 на 0 (+)
         Фактический результат:
         Код ответа - 200 ("OK")
         Флаг доступа пользователя access меняется с 1 на 0
         """

        user_db = self.mysql.session.query(Users).order_by(Users.password).filter_by(access=1).first()
        username = user_db.username

        assert user_db.access == 1, "Необходим пользователь с флагом доступа == 1"

        response = self.post_block_user(username)

        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(username=username).first()

        assert user_db.access == 0, "После блокировки флаг доступа access должен == 0"
        assert response.status_code == 200, "Код ответа приложения должен быть 200"
        assert json.loads(response.text) == {
            "detail": "User was blocked",
            "status": ""
        }, "Тело ответа приложения не соотв. ожидаемому"

        self.post_unblock_user(username)

    @allure.title("Блокировка уже заблокированного пользователя")
    @pytest.mark.API
    def test_post_block_already_blocked_user(self):
        """
         Тестирование: Блокировка уже заблокированного пользователя
         Эндпоинт: POST http://127.0.0.1:8086/api/user/{username}/block
         Предусловия: Авторизация, заблокировать рандомного пользователя
         Шаги:
         1. Вытащить из БД значение username, access для заблокированного пользователя
         2. Отправка запроса по API для смены флага доступа (блокировки пользователя) - POST
         http://127.0.0.1:8086/api/user/{username}/block
         3. Вернуть флаг access в изначальное состояние (разблокировать пользователя)
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (+)
         Информативное сообщение, о том, что пользователь уже заблокирован (+)
         Фактический результат:
         Код ответа - 400 ("BAD REQUEST")
         Информативное сообщение, о том, что пользователь уже заблокирован
         """

        user_db = self.mysql.session.query(Users).order_by(Users.password).filter_by(access=1).first()
        username = user_db.username

        self.post_block_user(username)

        self.mysql.session.commit()

        response = self.post_block_user(username)

        assert response.status_code == 400, "Код ответа приложения должен быть 400"
        assert json.loads(response.text) == {
            "detail": "User is already blocked",
            "status": "failed"
        }, "Тело ответа приложения не соотв. ожидаемому"

        self.post_unblock_user(username)

    @allure.title("Разблокировка ранее заблокированного пользователя")
    @pytest.mark.API
    def test_post_unblock_blocked_user_bug(self):
        """
         Тестирование: Разблокировка ранее заблокированного пользователя
         Эндпоинт: POST http://127.0.0.1:8086/api/user/{username}/accept
         Предусловия: Авторизация, заблокировать рандомного пользователя
         Шаги:
         1. Вытащить из БД значение username, access для заблокированного пользователя (access == 0)
         2. Отправка запроса по API для смены флага доступа (разблокировки пользователя) - POST
         http://127.0.0.1:8086/api/user/{username}/accept
         Ожидаемый результат:
         Код ответа - 200 ("OK") (+)
         Информативное корректное сообщение, о том, что пользователь разблокирован (-)
         Фактический результат:
         Код ответа - 200 ("OK") (+)
         Информативное корректное сообщение, о том, что пользователь разблокирован
         """

        user_db = self.mysql.session.query(Users).order_by(Users.password).filter_by(access=1).first()
        username = user_db.username

        self.post_block_user(username)

        self.mysql.session.commit()

        response = self.post_unblock_user(username)

        assert response.status_code == 200, "Код ответа приложения должен быть 200"
        assert json.loads(response.text) == {
            "detail": "User access granted",
            "status": ""
        }, "Тело ответа приложения не соотв. ожидаемому. В 'status' не должно быть значение 'failed'"

    @allure.title("Разблокировка ранее разблокированного пользователя")
    @pytest.mark.API
    def test_post_unblock_unblocked_user(self):
        """
         Тестирование: Разблокировка уже разблокированного пользователя
         Эндпоинт: POST http://127.0.0.1:8086/api/user/{username}/accept
         Предусловия: Авторизация
         Шаги:
         1. Вытащить из БД значение username, access для разблокированного пользователя (access == 1)
         2. Отправка запроса по API для смены флага доступа (разблокировки пользователя) - POST
         http://127.0.0.1:8086/api/user/{username}/accept
         Ожидаемый результат:
         Код ответа - 400 ("BAD REQUEST") (+)
         Информативное корректное сообщение, о том, что пользователь ранее уже разблокирован (+)
         Фактический результат:
         Код ответа - 400 ("BAD REQUEST")
         Информативное корректное сообщение, о том, что пользователь ранее уже разблокирован
         """

        user_db = self.mysql.session.query(Users).order_by(Users.password).filter_by(access=1).first()
        username = user_db.username

        response = self.post_unblock_user(username)

        assert response.status_code == 400, "Код ответа приложения должен быть 400"
        assert json.loads(response.text) == {
            "detail": "User is already active",
            "status": "failed"
        }, "Тело ответа приложения не соотв. ожидаемому"

    @allure.title("Получение статуса приложения")
    @pytest.mark.API
    def test_get_status(self):
        """
         Тестирование: Получение статуса приложения
         Эндпоинт: GET http://127.0.0.1:8086/status
         Предусловия: Поднятие приложения
         Шаги:
         1. Отправить запрос по API для получения статуса - GET http://127.0.0.1:8086/status
         Ожидаемый результат:
         Код ответа - 200 ("ОК") (+)
         Информативное корректное сообщение, о том, что приложение запущено (+)
         Фактический результат:
         Код ответа - 200 ("OK")
         Информативное корректное сообщение, о том, что приложение запущено
         """

        response = self.get_status()

        assert response.status_code == 200, "Код ответа приложения должен быть 200"
        assert json.loads(response.text) == {
            "status": "ok"
        }, "Тело ответа приложения не соотв. ожидаемому"

    @allure.title("Получение VK ID реального пользователя (mock)")
    @pytest.mark.API
    def test_get_vk_id_for_real_user(self):
        """
         Тестирование: Получение VK ID реального пользователя (mock)
         Эндпоинт: GET http://<VK_URL>/vk_id/<username>
         Предусловия: Запущен контейнер с моком, запущено приложение, mock корректно работает в приложении (в правом
         верхнем углу виден VK ID)
         Шаги:
         1. Достать из БД username какого-либо реального пользователя
         2. Отправить запрос по API для получения VK_ID - GET http://<VK_URL>/vk_id/{username}
         Ожидаемый результат:
         Код ответа - 200 ("ОК") (+)
         В response.body содержится корректное значени VK_ID для текущего пользователя  (+)
         Фактический результат:
         Код ответа - 200 ("OK")
         В response.body содержится корректное значени VK_ID для текущего пользователя
         """

        user_db = self.mysql.session.query(Users).order_by(Users.password).filter_by(access=1).first()
        username = user_db.username

        response = self.get_vk_id_from_mock(username)

        assert response.status_code == 200, "Код ответа приложения должен быть 200"
        assert re.match("\d{10}", json.loads(response.text)["vk_id"]), "VK_ID должно представлять из себя 10 " \
                                                                       "рандомных цифр"

    @allure.title("Получение VK ID несуществующего пользователя (mock)")
    @pytest.mark.API
    def test_get_vk_id_for_null_user(self):
        """
         Тестирование: Получение VK ID несущетсвующего (None) пользователя (mock)
         Эндпоинт: GET http://<VK_URL>/vk_id/<username>
         Предусловия: Запущен контейнер с моком, запущено приложение, mock корректно работает в приложении (в правом
         верхнем углу виден VK ID)
         Шаги:
         1. Отправить запрос по API для получения VK_ID - GET http://<VK_URL>/vk_id/{username}; В кач-ве {username}
         использовать сущность языка Python - None
         Ожидаемый результат:
         Код ответа - 404 ("NOT FOUND") (+)
         Выводится информативное сообщение, что VK_ID для рассматриваемого пользователя не найдено  (+)
         Фактический результат:
         Код ответа - 404 ("NOT FOUND")
         Выводится информативное сообщение, что VK_ID для рассматриваемого пользователя не найдено
         """

        username = None

        response = self.get_vk_id_from_mock(username)

        assert response.status_code == 404, "Код ответа приложения должен быть 404"
        assert response.text.replace('\n', '') == '"Not found"', "Тело ответа приложения не соотв. ожидаемому"


class TestApiUnauthorizedUser(BaseApi):
    @allure.title("Создание пользовательских данных (без middle-name)")
    @pytest.fixture(scope='function')
    def create_user_data_without_middle_name(self):
        user_info = UserInfo()
        user_data = user_info.create_user_data()
        human_data = user_info.create_human_data()
        complex_data = {**user_data, **human_data}
        return complex_data

    @allure.title("Авторизация с помощью верных данных")
    @pytest.mark.API
    def test_post_auth_correct_data(self):
        """
         Тестирование: Авторизация с помощью верных данных
         Эндпоинт: POST http://127.0.0.1:8086/login
         Предусловия: Пользователь не авторизован, известны логин/пароль для тестирования авторизации
         Шаги:
         1. Отправить запрос по API для авторизации - POST http://127.0.0.1:8086/login
         Ожидаемый результат:
         Код ответа - 302 ("FOUND") (+)
         Пользователь авторизовался (открывается страница с url /welcome) (+)
         Фактический результат:
         Код ответа - 302 ("FOUND") (+)
         Пользователь авторизовался (открывается страница с url /welcome)
         """
        self.api_client.session.cookies.clear()

        data = {
            'username': "nikita",
            'password': "test",
        }

        response = self.api_client.auth_login_cookies(data=data)

        self.api_client.session.cookies.clear()

        assert response.status_code == 302, "Код ответа приложения должен быть 302"
        assert dict_from_cookiejar(response.cookies)['session']

    @allure.title("Авторизация с помощью неверных данных")
    @pytest.mark.API
    @pytest.mark.parametrize('login, password', [('error', 'error'), ('nikita', 'testik'), ('nik', 'beast')])
    def test_post_auth_invalid_data_bug(self, login, password):
        """
         Тестирование: Авторизация с помощью неверных данных
         Эндпоинт: POST http://127.0.0.1:8086/login
         Предусловия: Пользователь не авторизован, для авторизации используется неверная комбинация логина/пароля;
         рассмотреть варианты, когда логин/пароль действительно существуют в БД, однако второй элемент из комбинации
         - нет
         Шаги:
         1. Отправить запрос по API для авторизации - POST http://127.0.0.1:8086/login
         Ожидаемый результат:
         Код ответа - 401 ("UNAUTHORIZED") (-)
         Пользователь не сумел авторизоваться, сервер возвращает адекватную ошибку и сообщение (-)
         Фактический результат:
         Код ответа - 200 ("OK") (-)
         Пользователь не сумел авторизоваться, сервер возвращает адекватную ошибку и сообщение (-)
         """
        self.api_client.session.cookies.clear()

        data = {
            'username': login,
            'password': password
        }

        response = self.api_client.auth_login_cookies(data=data)

        assert response.status_code == 401, """Код ответа приложения должен быть 401... Здесь что-то странное: отвечать  
                                             200 - на неудачную авторизацию явно не ок, тем более - куки пустые; 
                                             кроме того бывает, 
                                             когда при неверной комбинации возвраащет 401"""

    @allure.title("Очистка сессии после логаута")
    @pytest.mark.API
    def test_post_logout(self):
        """
         Тестирование: Очистка сесии после логаута
         Эндпоинт: GET http://127.0.0.1:8086/logout
         Предусловия: Пользователь не авторизован, известны логин/пароль для тестирования авторизации
         Шаги:
         1. Отправить запрос по API для авторизации - POST http://127.0.0.1:8086/login
         2. Отправить запрос по API для логаута - POST http://127.0.0.1:8086/logout
         Ожидаемый результат:
         Код ответа - 302 ("FOUND") (+)
         Пользователь разлогинился, сессионные куки пусты (+)
         Фактический результат:
         Код ответа - 302 ("FOUND")
         Пользователь разлогинился, сессионные куки пусты
         """
        self.api_client.session.cookies.clear()

        data = {
            'username': "nikita",
            'password': "test",
        }

        response_auth = self.api_client.auth_login_cookies(data=data)
        assert dict_from_cookiejar(response_auth.cookies)['session']

        response_logout = self.get_logout()

        assert response_logout.status_code == 302, "Код ответа приложения должен быть 302"
        assert not dict_from_cookiejar(response_logout.cookies)

    @allure.title("Создание пользователя без авторизации")
    @pytest.mark.API
    def test_post_create_user_without_auth(self, create_user_data_without_middle_name):
        """
         Тестирование: Очистка сесии после логаута
         Эндпоинт: POST http://127.0.0.1:8086/api/user
         Предусловия: Пользователь не авторизован
         Шаги:
         1. Отправить запрос по API для создания пользователя - POST http://127.0.0.1:8086/api/user
         Ожидаемый результат:
         Код ответа - 401 ("UNAUTHORIZED") (+)
         Фактический результат:
         Код ответа - 401 ("UNAUTHORIZED")
         """
        self.api_client.session.cookies.clear()

        complex_user_data = create_user_data_without_middle_name
        response = self.post_create_user(complex_user_data)

        assert response.status_code == 401, "Код ответа приложения должен быть 401"

    @allure.title("Удаление пользователя без авторизации")
    @pytest.mark.API
    def test_delete_user_without_auth(self, create_user_data_without_middle_name):
        """
         Тестирование: Удаление пользователя без авторизации
         Эндпоинт: DELETE http://127.0.0.1:8086/api/user/{username}
         Предусловия: Пользователь не авторизован, взять username пользователя уже имеющегося в БД
         Шаги:
         1. Отправить запрос по API для создания пользователя - DELETE http://127.0.0.1:8086/api/user/{username}
         Ожидаемый результат:
         Код ответа - 401 ("UNAUTHORIZED") (+)
         Фактический результат:
         Код ответа - 401 ("UNAUTHORIZED")
         """
        self.api_client.session.cookies.clear()

        response = self.delete_user("nikita")

        assert response.status_code == 401, "Код ответа приложения должен быть 401"

    @allure.title("Смена пароля без авторизации")
    @pytest.mark.API
    def test_put_change_password_without_auth(self, create_user_data_without_middle_name):
        """
         Тестирование: Очистка сесии после логаута
         Эндпоинт: PUT http://127.0.0.1:8086/api/user/{username}/change-password
         Предусловия: Пользователь не авторизован, взять username уже имеющегося пользователя из БД
         Шаги:
         1. Отправить запрос по API для смены пользователя - PUT http://127.0.0.1:8086/api/user/{
         username}/change-password
         Ожидаемый результат:
         Код ответа - 401 ("UNAUTHORIZED") (+)
         Фактический результат:
         Код ответа - 401 ("UNAUTHORIZED")
         """
        self.api_client.session.cookies.clear()

        response = self.put_change_password("nikita", "test")

        assert response.status_code == 401, "Код ответа приложения должен быть 401"

    @allure.title("Блокировка пользователя без авторизации")
    @pytest.mark.API
    def test_post_block_without_auth(self):
        """
         Тестирование: Блокировка пользователя
         Эндпоинт: POST http://127.0.0.1:8086/api/user/{username}/block
         Предусловия: Пользователь не авторизован, вытащить пользователя из БД с access == 1
         Шаги:
         1. Вытащить из БД значение username, access для любого пользователя
         2. Отправка запроса по API для смены флага доступа (блокировки пользователя) - POST
         http://127.0.0.1:8086/api/user/{username}/block
         Ожидаемый результат:
         Код ответа - 401 ("UNAUTHORIZED") (+)
         Фактический результат:
         Код ответа - 401 ("UNAUTHORIZED")
         """

        user_db = self.mysql.session.query(Users).order_by(Users.password).filter_by(access=1).first()
        username = user_db.username

        assert user_db.access == 1, "Необходим пользователь с флагом доступа == 1"

        self.api_client.session.cookies.clear()
        response = self.post_block_user(username)

        assert response.status_code == 401, "Код ответа приложения должен быть 401"

    @allure.title("Разблокировка пользователя без авторизации")
    @pytest.mark.API
    def test_post_unblock_without_auth(self):
        """
         Тестирование: Разблокировка пользователя без авторизации
         Эндпоинт: POST http://127.0.0.1:8086/api/user/{username}/block
         Предусловия: Пользователь не авторизован, вытащить пользователя из БД с access == 1
         Шаги:
         1. Вытащить из БД значение username, access для любого пользователя
         2. Отправка запроса по API для смены флага доступа (блокировки пользователя) - POST
         http://127.0.0.1:8086/api/user/{username}/block
         Ожидаемый результат:
         Код ответа - 401 ("UNAUTHORIZED") (+)
         Фактический результат:
         Код ответа - 401 ("UNAUTHORIZED")
         """

        user_db = self.mysql.session.query(Users).order_by(Users.password).filter_by(access=1).first()
        username = user_db.username

        self.post_block_user(username)

        self.mysql.session.commit()

        self.post_unblock_user(username)

        self.api_client.session.cookies.clear()
        response = self.post_unblock_user(username)

        assert response.status_code == 401, "Код ответа приложения должен быть 401"

    @allure.title("Получение статуса приложения без авторизации")
    @pytest.mark.API
    def test_get_status_without_auth(self):
        """
         Тестирование: Получение статуса приложения
         Эндпоинт: GET http://127.0.0.1:8086/status
         Предусловия: Поднятие приложения, пользователь не авторизован
         Шаги:
         1. Отправить запрос по API для получения статуса - GET http://127.0.0.1:8086/status
         Ожидаемый результат:
         Код ответа - 200 ("ОК") (+)
         Информативное корректное сообщение, о том, что приложение запущено (+)
         Фактический результат:
         Код ответа - 200 ("OK")
         Информативное корректное сообщение, о том, что приложение запущено
         """

        self.api_client.session.cookies.clear()
        response = self.get_status()

        assert response.status_code == 200, "Код ответа приложения должен быть 200"
        assert json.loads(response.text) == {
            "status": "ok"
        }, "Тело ответа приложения не соотв. ожидаемому"

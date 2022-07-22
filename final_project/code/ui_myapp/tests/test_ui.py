import re

import pytest
from locators.static_locators import *

from final_project.code.credentials.static import *
from final_project.code.mysql.utils.models import Users
from final_project.code.tools.randomizer import RandomGenerate
from final_project.code.ui_myapp.pages.welcome_page import *
from final_project.code.ui_myapp.tests.base_ui import BaseCase, BaseCaseLogin

MAX_RETRY_COUNT = 3


class TestUIUnauthorizedUserAuthPage(BaseCase):
    @allure.title('Страница авторизации. Корректные данные и успешная авторизация')
    @pytest.mark.UI
    def test_auth_page_correct_data(self):
        """
         Тестирование: Авторизация
         Предусловия: Корректные данные
         Шаги:
         1. Ввести данные через UI
         Ожидаемый результат:
         Успешный вход на /welcome (+)
         Фактический результат:
         Успешный вход на /welcome
         """
        self.auth_page.login()

        assert self.driver.current_url == WelcomePage.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/welcome/'"

    @allure.title('Страница авторизации. Некорректные данные(login)/неуспешная авторизация')
    @pytest.mark.UI
    def test_auth_page_invalid_data_username(self):
        """
         Тестирование: Авторизация
         Предусловия: Некорректные данные(login)
         Шаги:
         1. Ввести данные через UI
         Ожидаемый результат:
         Неуспешный вход, пользователь остается на /login (+)
         Pop-up, уведомляющий пользователя о неверной комбинации логина/пароля (+)
         Фактический результат:
         Неуспешный вход, пользователь остается на /login
         Pop-up, уведомляющий пользователя о неверной комбинации логина/пароля
        """
        self.auth_page.login(username=RandomGenerate.generate_random_user_name())

        assert self.driver.current_url == self.auth_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/login'"
        self.auth_page.find_pop_up_invalid_auth_message()

    @allure.title('Страница авторизации. Неккоректные данные(password)/неуспешная авторизация')
    @pytest.mark.UI
    def test_auth_page_invalid_data_password(self):
        """
        Тестирование: Авторизация
        Предусловия: Некорректные данные (password)
        Шаги:
        1. Ввести данные через UI
        Ожидаемый результат:
        Неуспешный вход, пользователь остается на /login (+)
        Pop-up, уведомляющий пользователя о неверной комбинации логина/пароля(+)
        Фактический результат:
        Неуспешный вход, пользователь остается на /login
        Pop-up, уведомляющий пользователя о неверной комбинации логина/пароля
        """
        self.auth_page.login(username=RandomGenerate.generate_random_password())

        assert self.driver.current_url == self.auth_page.url, f"URL должен быть 'http://http://{APP_HOST}:" \
                                                              f"{APP_PORT}/login'"
        self.auth_page.find_pop_up_invalid_auth_message()

    @allure.title('Страница авторизации. Валидация длины имени')
    @pytest.mark.UI
    def test_auth_page_invalid_data_password(self):
        """
        Тестирование: Авторизация
        Предусловия: Некорректные данные (длина имени меньше минимально допустимой)
        Шаги:
        1. Ввести данные через UI
        Ожидаемый результат:
        Неуспешный вход, пользователь остается на /login (+)
        Pop-up, уведомляющий пользователя (+)
        Фактический результат:
        Неуспешный вход, пользователь остается на /login (+)
        Pop-up, уведомляющий пользователя (+)
        """
        username = RandomGenerate.generate_random_password(1, 5)
        len_username_as_str = str(len(username))

        self.auth_page.login(username=username)

        assert self.driver.current_url == self.auth_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}//login'"
        assert f'Минимально допустимое количество символов: 6. Длина текста сейчас: {len_username_as_str}.' == \
               self.auth_page.find_pop_up_invalid_login_message()

    @allure.title('Страница авторизации. Value в placeholder username')
    @pytest.mark.UI
    def test_auth_page_value_username(self):
        """
        Тестирование: Авторизация. Value в placeholder username
        Шаги:
        1. Через UI посмотреть на "подсказку" поля username
        Ожидаемый результат:
        1. Подсказка совпадает с полем - Username (+)
        Фактический результат:
        1. Подсказка совпадает с полем - Username
        """
        self.auth_page.get_drive()
        assert 'Username' == self.auth_page.find(AuthPageLocators.QUERY_PLACEHOLDER_USER_NAME).get_attribute(
            'placeholder')

        assert self.driver.current_url == self.auth_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/login'"

    @allure.title('Страница авторизации. Value в placeholder password')
    @pytest.mark.UI
    def test_auth_page_value_password(self):
        """
        Тестирование: Авторизация. Value в placeholder password
        Шаги:
        1. Через UI посмотреть на "подсказку" поля password
        Ожидаемый результат:
        1. Подсказка совпадает с полем - Password (+)
        Фактический результат:
        1. Подсказка совпадает с полем - Password
        """
        self.auth_page.get_drive()
        assert 'Password' == self.auth_page.find(AuthPageLocators.QUERY_PLACEHOLDER_PASSWORD).get_attribute(
            'placeholder')

        assert self.driver.current_url == self.auth_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/login'"

    @allure.title('Страница авторизации. Переход на страницу регистрации')
    @pytest.mark.UI
    def test_auth_page_redirect_to_reg_page(self):
        """
        Тестирование: Авторизация. Переход на страницу регистрации
        Предусловия:
        Шаги:
        1. Нажать через UI на линк регистрации
        Ожидаемый результат:
        Линк действительно ведет на страницу регистрации /reg (+)
        Фактический результат:
        Линк действительно ведет на страницу регистрации /reg
        """
        self.auth_page.get_drive()
        self.auth_page.search_click(AuthPageLocators.QUERY_LOGIN)

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"


class TestUIUnauthorizedUserRegistrationPage(BaseCase):

    @allure.title('БАГ! Страница регистрации. Валидные данные (c middle-name). Успешная регистрация')
    @pytest.mark.UI
    def test_reg_page_success_with_middle_name_bug(self, create_user_data_with_middle_name):
        """
        Тестирование: Регистрация. Валидные данные
        Предусловия: Сгенерировать валидные данные
        Шаги:
        1. Заполнить через UI все поля регистрации
        2. Нажать на чекбокс
        Ожидаемый результат:
        1. Пользователю открывается страница /welcome (+)
        2. Пользователь с указанными данными создается в БД (-)
        Фактический результат:
        1. Пользователю открывается страница /welcome
        2. Пользователь с указанными данными создается в БД
        """

        complex_user_data = create_user_data_with_middle_name
        self.registration_page.registration(complex_user_data, middle_name_option=1)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

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

        assert user_db.access == 1, "Access по умолчанию должен быть равен 1!"
        assert user_db.active == 0, "Active по умолчанию должен быть равен 0!"
        assert self.driver.current_url == WelcomePage.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/welcome/'"
        assert user_db.middle_name == complex_user_data['middle_name'], f"Отчества не совпадают: В БД" \
                                                                        f" {user_db.middle_name}; " \
                                                                        f"Отправлено в request body " \
                                                                        f"{complex_user_data['middle_name']}"

    @allure.title('Страница регистрации. Валидные данные (без middle-name). Успешная регистрация')
    @pytest.mark.UI
    def test_reg_page_success_without_middle_name(self, create_user_data_with_middle_name):
        """
        Тестирование: Регистрация. Валидные данные, без middle-name
        Предусловия: Сгенерировать валидные данные
        Шаги:
        1. Заполнить через UI все поля регистрации
        2. Нажать на чекбокс
        Ожидаемый результат:
        1. Пользователю открывается страница /welcome
        2. Пользователь с указанными данными создается в БД (middle-name NULL)
        Фактический результат:
        1. Пользователю орывается страница /welcome
        2. Пользователь с указанными данными создается в БД
        """

        complex_user_data = create_user_data_with_middle_name
        self.registration_page.registration(complex_user_data)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

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

        assert user_db.middle_name is None, "Отчество должно быть пустым"
        assert user_db.access == 1, "Access по умолчанию должен быть равен 1!"
        assert user_db.active == 0, "Active по умолчанию должен быть равен 0!"
        assert self.driver.current_url == WelcomePage.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/welcome/'"

    @allure.title('Страница регистрации. Pop-up "заполните это поле" при пустом Name')
    @pytest.mark.UI
    def test_reg_page_validation_empty_name(self, create_user_data_with_middle_name):
        """
        Тестирование: Регистрация. Пустое поле name
        Предусловия: Сгенерировать валидные данные
        Шаги:
        1. Заполнить через UI все поля регистрации, кроме name
        2. Нажать на чекбокс
        Ожидаемый результат:
        1. Пользователь остается на странице /reg (+)
        2. Показывается pop-up, уведомляющий о пустом поле name (+)
        3. Пользователь с указанными данными не создается в БД (+)
        Фактический результат:
        1. Пользователь остается на странцие /reg
        2. Показывается pop-up, уведомляющий о пустом поле name
        3. Пользователь с указанными данными не создается в БД
        """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data.pop("name")
        self.registration_page.registration(complex_user_data)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"
        assert self.registration_page.find_pop_up_empty_req_field(RegistrationPageLocators.QUERY_PLACEHOLDER_NAME) == \
               "Заполните это поле."
        assert user_db is None, "Не должно быть занесено в БД какой-либо информации о пользователе"

    @allure.title('Страница регистрации. Pop-up "заполните это поле" при пустом Surname')
    @pytest.mark.UI
    def test_reg_page_validation_empty_surname(self, create_user_data_with_middle_name):
        """
        Тестирование: Регистрация. Пустое поле Surname
        Предусловия: Сгенерировать валидные данные
        Шаги:
        1. Заполнить через UI все поля регистрации, кроме name
        2. Нажать на чекбокс
        Ожидаемый результат:
        1. Пользователь остается на странице /reg (+)
        2. Показывается pop-up, уведомляющий о пустом поле surname (+)
        3. Пользователь с указанными данными не создается в БД (+)
        Фактический результат:
        1. Пользователь остается на странице /reg
        2. Показывается pop-up, уведомляющий о пустом поле surname
        3. Пользователь с указанными данными не создается в БД
        """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data.pop("surname")
        self.registration_page.registration(complex_user_data)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"
        assert self.registration_page.find_pop_up_empty_req_field(RegistrationPageLocators.QUERY_PLACEHOLDER_SURNAME) \
               == \
               "Заполните это поле."
        assert user_db is None, "Не должно быть занесено в БД какой-либо информации о пользователе"

    @allure.title('Страница регистрации. Pop-up "заполните это поле" при пустом Surname')
    @pytest.mark.UI
    def test_reg_page_validation_empty_username(self, create_user_data_with_middle_name):
        """
        Тестирование: Регистрация. Пустое поле username
        Предусловия: Сгенерировать валидные данные
        Шаги:
        1. Заполнить через UI все поля регистрации, кроме name
        2. Нажать на чекбокс
        Ожидаемый результат:
        1. Пользователь остается на странице /reg (+)
        2. Показывается pop-up, уведомляющий о пустом поле name (+)
        3. Пользователь с указанными данными не создается в БД (+)
        Фактический результат:
        1. Пользователь остается на странице /reg
        2. Показывается pop-up, уведомляющий о пустом поле name
        3. Пользователь с указанными данными не создается в БД
        """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data.pop("username")
        self.registration_page.registration(complex_user_data)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"
        assert self.registration_page.find_pop_up_empty_req_field(
            RegistrationPageLocators.QUERY_PLACEHOLDER_USER_NAME) \
               == \
               "Заполните это поле."
        assert user_db is None, "Не должно быть занесено в БД какой-либо информации о пользователе"

    @allure.title('Страница регистрации. Pop-up "заполните это поле" при пустом email')
    @pytest.mark.UI
    def test_reg_page_validation_empty_email(self, create_user_data_with_middle_name):
        """
        Тестирование: Регистрация. Пустое поле email
        Предусловия: Сгенерировать валидные данные
        Шаги:
        1. Заполнить через UI все поля регистрации, кроме email
        2. Нажать на чекбокс
        Ожидаемый результат:
        1. Пользователь остается на странице /reg (+)
        2. Показывается pop-up, уведомляющий о пустом поле email (+)
        3. Пользователь с указанными данными не создается в БД (+)
        Фактический результат:
        1. Пользователь остается на странице /reg
        2. Показывается pop-up, уведомляющий о пустом поле email
        3. Пользователь с указанными данными не создается в БД
        """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data.pop("email")
        self.registration_page.registration(complex_user_data)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['username']).first()

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"
        assert self.registration_page.find_pop_up_text(
            RegistrationPageLocators.QUERY_INCORRECT_EMAIL_LENGTH) == 'Incorrect email length', "Должен быть такой pop-up!"
        assert user_db is None, "Не должно быть занесено в БД какой-либо информации о пользователе"

    @allure.title('Страница регистрации. Pop-up "заполните это поле" при пустом password')
    @pytest.mark.UI
    def test_reg_page_validation_empty_password(self, create_user_data_with_middle_name):
        """
        Тестирование: Регистрация. Пустое поле password
        Предусловия: Сгенерировать валидные данные
        Шаги:
        1. Заполнить через UI все поля регистрации, кроме password
        2. Нажать на чекбокс
        Ожидаемый результат:
        1. Пользователь остается на странице /reg (+)
        2. Показывается pop-up, уведомляющий о пустом поле password (+)
        3. Пользователь с указанными данными не создается в БД (+)
        Фактический результат:
        1. Пользователь остается на странице /reg
        2. Показывается pop-up, уведомляющий о пустом поле password
        3. Пользователь с указанными данными не создается в БД
        """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data.pop("password")
        self.registration_page.registration(complex_user_data)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['username']).first()

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"
        assert self.registration_page.find_pop_up_empty_req_field(
            RegistrationPageLocators.QUERY_PLACEHOLDER_PASSWORD) \
               == \
               "Заполните это поле."
        assert user_db is None, "Не должно быть занесено в БД какой-либо информации о пользователе"

    @allure.title('Страница регистрации. Pop-up "заполните это поле" при пустом repeat-password')
    @pytest.mark.UI
    def test_reg_page_validation_empty_repeat_password(self, create_user_data_with_middle_name):
        """
          Тестирование: Регистрация. Пустое поле repeat password
          Предусловия: Сгенерировать валидные данные
          Шаги:
          1. Заполнить через UI все поля регистрации, кроме repeat password
          2. Нажать на чекбокс
          Ожидаемый результат:
          1. Пользователь остается на странице /reg (+)
          2. Показывается pop-up, уведомляющий о пустом поле repeat password (+)
          3. Пользователь с указанными данными не создается в БД (+)
          Фактический результат:
          1. Пользователь остается на странице /reg
          2. Показывается pop-up, уведомляющий о пустом поле repeat password
          3. Пользователь с указанными данными не создается в БД
        """
        complex_user_data = create_user_data_with_middle_name
        self.registration_page.registration(complex_user_data, empty_rep_password_option=1)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['username']).first()

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"
        assert self.registration_page.find_pop_up_text(
            RegistrationPageLocators.QUERY_PASSWORDS_MUST_MATCH) == "Passwords must match", "Должен быть такой pop-up!"
        assert user_db is None, "Не должно быть занесено в БД какой-либо информации о пользователе"

    @allure.title('Страница регистрации. Pop-up "заполните это поле" при пустом чекбоксе')
    @pytest.mark.UI
    def test_reg_page_validation_empty_checkbox(self, create_user_data_with_middle_name):
        """
          Тестирование: Регистрация. Пустой чекбокс
          Предусловия: Сгенерировать валидные данные
          Шаги:
          1. Заполнить через UI все поля регистрации
          2. Не нажимать на чекбокс
          Ожидаемый результат:
          1. Пользователь остается на странице /reg (+)
          2. Показывается pop-up, уведомляющий о пустом чекбоксе (+)
          3. Пользователь с указанными данными не создается в БД (+)
          Фактический результат:
          1. Пользователь остается на странице /reg
          2. Показывается pop-up, уведомляющий о пустом чекбоксе
          3. Пользователь с указанными данными не создается в БД
        """
        complex_user_data = create_user_data_with_middle_name
        self.registration_page.registration(complex_user_data, checkbox_option=0)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['username']).first()

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"
        assert self.registration_page.find_pop_up_empty_req_field(
            RegistrationPageLocators.QUERY_CHECK_BOX) == "Чтобы продолжить, установите этот флажок."
        assert user_db is None, "Не должно быть занесено в БД какой-либо информации о пользователе"

    @allure.title('Страница регистрации. Pop-up "User already exists" при повторении username')
    @pytest.mark.UI
    def test_reg_page_validation_already_used_user(self, create_user_data_with_middle_name):
        """
          Тестирование: Регистрация. Username уже добавлен ранее в БД
          Предусловия: Сгенерировать валидные данные, заменить username на
          использованный ранее
          Шаги:
          1. Заполнить через UI все поля регистрации
          Ожидаемый результат:
          1. Пользователь остается на странице /reg (+)
          2. Показывается pop-up, уведомляющий о том, что username уже
          используется (+)
          3. Пользователь с указанными данными не создается в БД (+)
          Фактический результат:
          1. Пользователь остается на странице /reg
          2. Показывается pop-up, уведомляющий о том, что username уже
          используется
          3. Пользователь с указанными данными не создается в БД
        """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data['username'] = 'nikita'
        self.registration_page.registration(complex_user_data)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['email']).first()

        assert self.driver.current_url == self.registration_page.url, "URL должен быть f'http://{APP_HOST}:{APP_PORT}/reg'"
        assert self.registration_page.find_pop_up_text(
            RegistrationPageLocators.QUERY_USER_ALREADY_EXISTS) == "User already exist", "Должен быть такой pop-up!"
        assert user_db is None, "Не должно быть занесено в БД какой-либо информации о пользователе"

    @allure.title('БАГ! Страница регистрации. Pop-up "Email already exists" при повторении username')
    @pytest.mark.UI
    def test_reg_page_validation_already_used_email_bug(self, create_user_data_with_middle_name):
        """
          Тестирование: Регистрация. Email уже добавлен ранее в БД
          Предусловия: Сгенерировать валидные данные, заменить username на
          использованный ранее
          Шаги:
          1. Заполнить через UI все поля регистрации
          Ожидаемый результат:
          1. Пользователь остается на странице /reg (+)
          2. Показывается pop-up, уведомляющий о том, что email уже
          используется (-)
          3. Пользователь с указанными данными не создается в БД (+)
          Фактический результат:
          1. Пользователь остается на странице /reg (+)
          2. Показывается pop-up, о INTERNAL SERVER ERROR
          3. Пользователь с указанными данными не создается в БД (+)
        """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data['email'] = 'nik-stepanov-2001@bk.ru'
        self.registration_page.registration(complex_user_data)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['username']).first()

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"
        assert self.registration_page.find_pop_up_text(
            RegistrationPageLocators.QUERY_EMAIL_ALREADY_EXISTS) == "Email already exists", "Должен быть такой pop-up!"
        assert user_db is None, "Не должно быть занесено в БД какой-либо информации о пользователе"

    @allure.title('БАГ! Страница регистрации. Минимальная длина username. Этот тест имеет flucky сообщение!')
    @pytest.mark.UI
    def test_reg_page_validation_min_length_username_bug(self, create_user_data_with_middle_name):
        """
          Тестирование: Регистрация. Длина username меньше минимальной (6)
          Предусловия: Сгенерировать валидные данные
          Шаги:
          1. Заполнить через UI все поля регистрации
          Ожидаемый результат:
          1. Пользователь остается на странице /reg (+)
          2. Показывается pop-up, уведомляющий о том, что username меньше
          минимальной длины (6) (+)
          3. Пользователь с указанными данными не создается в БД (+)
          Фактический результат:
          1. Пользователь остается на странице /reg (+)
          2. Показывается pop-up, уведомляющий о том, что username уже
          используется (+)
          3. Пользователь с указанными данными не создается в БД (+)
        """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data["username"] = RandomGenerate.generate_random_password(1, 5)
        len_username_as_str = str(len(complex_user_data["username"]))
        self.registration_page.registration(complex_user_data)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['username']).first()

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"
        assert f'Минимально допустимое количество символов: 6. Длина текста сейчас: {len_username_as_str}.' == \
               self.registration_page.find_pop_up_empty_req_field(RegistrationPageLocators.QUERY_PLACEHOLDER_USER_NAME)
        assert user_db is None, "Не должно быть занесено в БД какой-либо информации о пользователе"

    @allure.title('Страница регистрации. Минимальная длина email')
    @pytest.mark.UI
    def test_reg_page_validation_min_length_email(self, create_user_data_with_middle_name):
        """
          Тестирование: Регистрация. Длина email меньше минимальной (6)
          Предусловия: Сгенерировать валидные данные
          Шаги:
          1. Заполнить через UI все поля регистрации
          Ожидаемый результат:
          1. Пользователь остается на странице /reg (+)
          2. Показывается pop-up, уведомляющий о том, что email меньше
          минимальной длины (6) (+)
          3. Пользователь с указанными данными не создается в БД (+)
          Фактический результат:
          1. Пользователь остается на странице /reg
          2. Показывается pop-up, уведомляющий о том, что email меньше мин. длины
          3. Пользователь с указанными данными не создается в БД
        """
        complex_user_data = create_user_data_with_middle_name
        complex_user_data["email"] = 'k@k.f'
        len_email_as_str = str(len(complex_user_data["email"]))
        self.registration_page.registration(complex_user_data)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['username']).first()

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"
        assert f'Минимально допустимое количество символов: 6. Длина текста сейчас: {len_email_as_str}.' == \
               self.registration_page.find_pop_up_empty_req_field(RegistrationPageLocators.QUERY_PLACEHOLDER_EMAIL)
        assert user_db is None, "Не должно быть занесено в БД какой-либо информации о пользователе"

    @allure.title('Страница регистрации. Не соотв. схеме email')
    @pytest.mark.UI
    @pytest.mark.parametrize("flag", [0, 1])
    def test_reg_page_validation_invalid_email_schema(self, create_user_data_with_middle_name, flag):
        """
          Тестирование: Регистрация. Email не соотв. схеме (имя+@+домен)
          Предусловия: Сгенерировать валидные данные
          Шаги:
          1. Заполнить через UI все поля регистрации
          Ожидаемый результат:
          1. Пользователь остается на странице /reg (+)
          2. Показывается pop-up, уведомляющий о том, что email не соотв. схеме (+)
          3. Пользователь с указанными данными не создается в БД (+)
          Фактический результат:
          1. Пользователь остается на странице /reg (+)
          2. Показывается pop-up, уведомляющий о том, что email не соотв. схеме
          3. Пользователь с указанными данными не создается в БД (+)
        """
        complex_user_data = create_user_data_with_middle_name
        if flag == 0:
            complex_user_data["email"] = RandomGenerate.generate_random_email(first_half=1)
        elif flag == 1:
            complex_user_data["email"] = RandomGenerate.generate_random_email(second_half=1)

        self.registration_page.registration(complex_user_data)
        self.mysql.session.commit()

        user_db = self.mysql.session.query(Users).filter_by(email=complex_user_data['username']).first()

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть http://{APP_HOST}:{APP_PORT}/reg"
        assert 'Invalid email address' == self.registration_page.find_pop_up_text(
            RegistrationPageLocators.QUERY_EMAIL_INVALID), "Должен быть такой pop-up!"
        assert user_db is None, "Не должно быть занесено в БД какой-либо информации о пользователе"

    @allure.title('Страница регистрации. Линк на авторизацию')
    @pytest.mark.UI
    def test_reg_page_link_to_auth_page(self):
        """
          Тестирование: Регистрация. Линк на страницу авторизации
          Шаги:
          1. Через UI нажать на линк авторизации
          Ожидаемый результат:
          1. Пользователь перенаправляется на страницу /login (+)
          Фактический результат:
          1. Пользователь остается на странице /login
        """
        self.registration_page.get_drive()
        self.registration_page.search_click(RegistrationPageLocators.QUERY_LOGIN)

        assert self.driver.current_url == self.auth_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/login'"

    @allure.title('Страница регистрации. Value в placeholder name')
    @pytest.mark.UI
    def test_reg_page_value_name(self):
        """
          Тестирование: Регистрация. Value в placeholder name
          Шаги:
          1. Через UI посмотреть на "подсказку" поля name
          Ожидаемый результат:
          1. Подсказка совпадает с полем - Name (+)
          Фактический результат:
          1. Подсказка совпадает с полем - Name
        """
        self.registration_page.get_drive()
        assert 'Name' == self.registration_page.find(RegistrationPageLocators.QUERY_PLACEHOLDER_NAME).get_attribute('placeholder')

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"

    @allure.title('Страница регистрации. Value в placeholder surname')
    @pytest.mark.UI
    def test_reg_page_value_surname(self):
        """
          Тестирование: Регистрация. Value в placeholder surname
          Шаги:
          1. Через UI посмотреть на "подсказку" поля surname
          Ожидаемый результат:
          1. Подсказка совпадает с полем - Surname (+)
          Фактический результат:
          1. Подсказка совпадает с полем - Surname
        """
        self.registration_page.get_drive()
        assert 'Surname' == self.registration_page.find(RegistrationPageLocators.QUERY_PLACEHOLDER_SURNAME).get_attribute(
            'placeholder')

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"

    @allure.title('БАГ! Страница регистрации. Value в placeholder midlename')
    @pytest.mark.UI
    def test_reg_page_value_midlename_bug(self):
        """
          Тестирование: Регистрация. Value в placeholder midlename
          Шаги:
          1. Через UI посмотреть на "подсказку" поля midlename
          Ожидаемый результат:
          1. Подсказка совпадает с полем - Midlename (-)
          Фактический результат:
          1. Подсказка совпадает с полем - Middddleeeename
        """
        self.registration_page.get_drive()
        assert 'Midlename' == self.registration_page.find(RegistrationPageLocators.QUERY_PLACEHOLDER_MIDDLE_NAME).get_attribute(
            'placeholder')

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"

    @allure.title('Страница регистрации. Value в placeholder username')
    @pytest.mark.UI
    def test_reg_page_value_username(self):
        """
          Тестирование: Регистрация. Value в placeholder username
          Шаги:
          1. Через UI посмотреть на "подсказку" поля username
          Ожидаемый результат:
          1. Подсказка совпадает с полем - Username (+)
          Фактический результат:
          1. Подсказка совпадает с полем - Username
        """
        self.registration_page.get_drive()
        assert 'Username' == self.registration_page.find(RegistrationPageLocators.QUERY_PLACEHOLDER_USER_NAME).get_attribute(
            'placeholder')

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"

    @allure.title('Страница регистрации. Value в placeholder email')
    @pytest.mark.UI
    def test_reg_page_value_email(self):
        """
          Тестирование: Регистрация. Value в placeholder email
          Шаги:
          1. Через UI посмотреть на "подсказку" поля email
          Ожидаемый результат:
          1. Подсказка совпадает с полем - Email (+)
          Фактический результат:
          1. Подсказка совпадает с полем - Email
        """
        self.registration_page.get_drive()
        assert 'Email' == self.registration_page.find(RegistrationPageLocators.QUERY_PLACEHOLDER_EMAIL).get_attribute(
            'placeholder')

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"

    @allure.title('Страница регистрации. Value в placeholder password')
    @pytest.mark.UI
    def test_reg_page_value_password(self):
        """
          Тестирование: Регистрация. Value в placeholder password
          Шаги:
          1. Через UI посмотреть на "подсказку" поля password
          Ожидаемый результат:
          1. Подсказка совпадает с полем - Password (+)
          Фактический результат:
          1. Подсказка совпадает с полем - Password
        """
        self.registration_page.get_drive()
        assert 'Password' == self.registration_page.find(RegistrationPageLocators.QUERY_PLACEHOLDER_PASSWORD).get_attribute(
            'placeholder')

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"

    @allure.title('Страница регистрации. Value в placeholder repeat password')
    @pytest.mark.UI
    def test_reg_page_value_repeat_password(self):
        """
          Тестирование: Регистрация. Value в placeholder repeat password
          Шаги:
          1. Через UI посмотреть на "подсказку" поля repeat password
          Ожидаемый результат:
          1. Подсказка совпадает с полем - Repeat password (+)
          Фактический результат:
          1. Подсказка совпадает с полем - Repeat password
        """
        self.registration_page.get_drive()
        assert "Repeat password" == self.registration_page.find(
            RegistrationPageLocators.QUERY_PLACEHOLDER_REPEAT_PASSWORD).get_attribute(
            'placeholder')

        assert self.driver.current_url == self.registration_page.url, f"URL должен быть 'http://{APP_HOST}:{APP_PORT}/reg'"


class TestUIUnauthorizedUserWelcomePage(BaseCase):

    @allure.title('Основная страница. Без авторизации')
    @pytest.mark.UI
    def test_main_page_without_auth(self):
        """
          Тестирование: Основная страница.
          Предусловия: Пользователь не авторизован
          Шаги:
          1. Через UI перейти на основную страницу /welcome
          Ожидаемый результат:
          1. Пользователь покажется pop-up, уведомляющий его, что эта страница доступна только авторизованному пол-лю
          (+)
          Фактический результат:
          1. Пользователь покажется pop-up, уведомляющий его, что эта страница доступна только авторизованному пол-лю
        """

        self.driver.get(url=WelcomePage.url)

        assert self.registration_page.find_pop_up_text(RegistrationPageLocators.QUERY_PAGE_AVAILABLE_TO_AUTH_USER) == \
               'This page is available only to authorized users', "Должен быть такой pop-up!"
        assert self.driver.current_url == f"http://{APP_HOST}:{APP_PORT}/login?next=/welcome/", f"URL должен быть 'http://" \
                                                                                                f"{APP_HOST}:" \
                                                                                                f"{APP_PORT}/login?next=/welcome/'"


class TestUIAuthorizedUserWelcomePage(BaseCaseLogin):

    @allure.title('Основная страница. Корректная Авторизация')
    @pytest.mark.UI
    def test_welcome_page(self):
        """
          Тестирование: Основная страница.
          Предусловия: Пользователь авторизован
          Шаги:
          1. Авторизоваться
          Ожидаемый результат:
          1. Пользователя редирекнет на основную страницу /welcome (+)
          Фактический результат:
          1. Пользователя редирекнет на основную страницу /welcome
        """

        assert self.driver.current_url == self.welcome_page.url, f"URL должен быть http://{APP_HOST}:{APP_PORT}/welcome/"

    @allure.title('Основная страница. Нажатие на кнопку с жуком (bug)')
    @pytest.mark.UI
    def test_welcome_page_click_on_image(self):
        """
          Тестирование: Основная страница. Нажатие на кнопку с жуком (bug)
          Предусловия: Пользователь авторизован
          Шаги:
          1. Нажать на кнопку с жуком
          Ожидаемый результат:
          1. Страница обновится, факт о языке Python снизу изменится (+)
          Фактический результат:
          1. Страница обновится, факт о языке Python снизу изменится
        """
        fact_text = self.welcome_page.click_on_image_bug()

        assert fact_text != self.welcome_page.find(WelcomePageLocators.QUERY_FACT).text
        assert self.driver.current_url == self.welcome_page.url, f"URL должен быть http://{APP_HOST}:{APP_PORT}/welcome/"

    @allure.title('Основная страница. Нажатие на кнопку HOME')
    @pytest.mark.UI
    def test_welcome_page_click_on_button_home(self):
        """
          Тестирование: Основная страница. Нажатие на кнопку HOME
          Предусловия: Пользователь авторизован
          Шаги:
          1. Нажатие на кнопку HOME
          Ожидаемый результат:
          1. Страница обновится, факт о языке Python снизу изменится (+)
          Фактический результат:
          1. Страница обновится, факт о языке Python снизу изменится
        """
        fact_text = self.welcome_page.click_on_button_home()

        assert fact_text != self.welcome_page.find(WelcomePageLocators.QUERY_FACT).text
        assert self.driver.current_url == self.welcome_page.url, f"URL должен быть http://{APP_HOST}:{APP_PORT}/welcome/"

    @allure.title('Основная страница. Нажатие на кнопку с Python')
    @pytest.mark.UI
    def test_welcome_page_click_on_python_image(self):
        """
          Тестирование: Основная страница. Нажатие на кнопку с Python
          Предусловия: Пользователь авторизован
          Шаги:
          1. Нажать на кнопку с Python
          Ожидаемый результат:
          1. Пользователя редирекнет на https://www.python.org/ (+)
          Фактический результат:
          1. Пользователя редирекнет на https://www.python.org/
        """
        self.welcome_page.search_click(WelcomePageLocators.QUERY_NAV_BAR_PYTHON)

        assert self.driver.current_url == "https://www.python.org/", "URL должен быть 'https://www.python.org/'"

    @allure.title('Основная страница. Нажатие на кнопку Python History в выпадающем меню кнопки Python: -> Python History')
    @pytest.mark.UI
    def test_welcome_page_click_on_python_history(self):
        """
          Тестирование: Основная страница. Наведение на кнопку с Python -> Нажатие на кнопку Python History
          Предусловия: Пользователь авторизован
          Шаги:
          1. Нажать на кнопку с Python
          Ожидаемый результат:
          1. Пользователя редирекнет на https://www.python.org/ (+)
          Фактический результат:
          1. Пользователя редирекнет на https://www.python.org/
        """
        self.welcome_page.click_on_python_history_in_python_button_menu()

        assert self.driver.current_url == "https://en.wikipedia.org/wiki/History_of_Python", \
            "URL должен быть 'https://en.wikipedia.org/wiki/History_of_Python'"

    @allure.title('Основная страница. Нажатие на кнопку About Flask в выпадающем меню кнопки Python: Python -> About Flask')
    @pytest.mark.UI
    def test_welcome_page_click_on_about_flask(self):
        """
          Тестирование: Основная страница. Наведение на кнопку с Python -> Нажатие на кнопку About Flask
          Предусловия: Пользователь авторизован
          Шаги:
          1. Нажать на кнопку с Python
          Ожидаемый результат:
          1. Открывается новое окно с  (новая вкладка) https://flask.palletsprojects.com/en/1.1.x/# (+)
          Фактический результат:
          1. Открывается новое окно с  (новая вкладка) https://flask.palletsprojects.com/en/1.1.x/#
        """
        self.welcome_page.click_on_about_flask_in_python_button_menu()
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)

        assert self.driver.current_url == "https://flask.palletsprojects.com/en/1.1.x/#", \
            "URL должен быть 'https://flask.palletsprojects.com/en/1.1.x/#"

    @allure.title('БАГ! Основная страница. Нажатие на кнопку Download Centos 7 в выпадающем меню кнопки Linux')
    @pytest.mark.UI
    def test_welcome_page_click_on_download_centos_bug(self):
        """
          Тестирование: Основная страница. Наведение на кнопку с Linux -> Нажатие на кнопку Download Centos 7
          Предусловия: Пользователь авторизован
          Шаги:
          1. Нажать на кнопку Download Centos 7 в меню кнопки Linux
          Ожидаемый результат:
          1. Пользователя редирекнет на (новая вкладка) https://www.centos.org/download/ (+)
          Фактический результат:
          1. Пользователя редирекнет на (новая вкладка) https://en.wikipedia.org/wiki/History_of_Python
        """
        self.welcome_page.click_on_download_centos_in_linux_button_menu()
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)

        assert self.driver.current_url == "https://www.centos.org/download/", \
            "URL должен быть https://www.centos.org/download/ Мы же качаем его! А не федору)"

    @allure.title('Основная страница. Нажатие на кнопку News в выпадающем меню кнопки Network: Network -> News')
    @pytest.mark.UI
    def test_welcome_page_click_on_network_news(self):
        """
          Тестирование: Основная страница. Наведение на кнопку с Network -> Нажатие на кнопку News в выпадающем меню
          Предусловия: Пользователь авторизован
          Шаги:
          1. Нажать на кнопку News в выпадающем меню кнопки Network
          Ожидаемый результат:
          1. Пользователя редирекнет на (новая вкладка) https://www.wireshark.org/news/ (+)
          Фактический результат:
          1. Пользователя редирекнет на (новая вкладка) https://www.wireshark.org/news/
        """
        self.welcome_page.click_on_news_in_network_button_menu()
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)

        assert self.driver.current_url == "https://www.wireshark.org/news/", \
            "URL должен быть https://www.wireshark.org/news/"

    @allure.title('Основная страница. Нажатие на кнопку Download в выпадающем меню кнопки Network: Network -> Download')
    @pytest.mark.UI
    def test_welcome_page_click_on_network_download(self):
        """
          Тестирование: Основная страница. Наведение на кнопку с Network -> Нажатие на кнопку Download в выпадающем меню
          Предусловия: Пользователь авторизован
          Шаги:
          1. Нажать на кнопку Download в выпадающем меню кнопки Network
          Ожидаемый результат:
          1. Пользователя редирекнет на (новая вкладка) https://www.wireshark.org/#download (+)
          Фактический результат:
          1. Пользователя редирекнет на (новая вкладка) https://www.wireshark.org/#download
        """
        self.welcome_page.click_on_download_in_network_button_menu()
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)

        assert self.driver.current_url == "https://www.wireshark.org/#download", \
            "URL должен быть https://www.wireshark.org/#download"

    @allure.title('Основная страница. Нажатие на кнопку Examples в выпадающем меню кнопки Network: Network -> Examples')
    @pytest.mark.UI
    def test_welcome_page_click_on_network_examples(self):
        """
          Тестирование: Основная страница. Наведение на кнопку с Network -> Нажатие на кнопку Examples в выпадающем меню
          Предусловия: Пользователь авторизован
          Шаги:
          1. Нажать на кнопку Download в выпадающем меню кнопки Examples
          Ожидаемый результат:
          1. Пользователя редирекнет (новая вкладка) на hhttps://hackertarget.com/tcpdump-examples/ (+)
          Фактический результат:
          1. Пользователя редирекнет (новая вкладка) на https://hackertarget.com/tcpdump-examples/
        """
        self.welcome_page.click_on_examples_in_network_button_menu()
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)

        assert self.driver.current_url == "https://hackertarget.com/tcpdump-examples/", \
            "URL должен быть https://hackertarget.com/tcpdump-examples/"

    @allure.title('Основная страница. Нажатие на картинку с Монитором')
    @pytest.mark.UI
    def test_welcome_page_click_on_image_laptop(self):
        """
          Тестирование: Основная страница. Нажатие на картинку с Монитором'
          Предусловия: Пользователь авторизован
          Шаги:
          1. Нажать на картинку с монитором
          Ожидаемый результат:
          1. Пользователя редирекнет (новая вкладка) на https://en.wikipedia.org/wiki/API (+)
          Фактический результат:
          1. Пользователя редирекнет (новая вкладка) на https://en.wikipedia.org/wiki/API
        """
        self.welcome_page.search_click(WelcomePageLocators.QUERY_IMAGE_LAPTOP)
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)

        assert self.driver.current_url == "https://en.wikipedia.org/wiki/API", \
            "URL должен быть https://en.wikipedia.org/wiki/API"

    @allure.title('Основная страница. Нажатие на картинку с Лупой')
    @pytest.mark.UI
    def test_welcome_page_click_on_image_loop(self):
        """
          Тестирование: Основная страница. Нажатие на картинку с Лупой
          Предусловия: Пользователь авторизован
          Шаги:
          1. Нажать на картинку с лупой
          Ожидаемый результат:
          1. Пользователя редирекнет (новая вкладка) на
          https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/ (+)
          Фактический результат:
          1. Пользователя редирекнет (новая вкладка) на
          https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/
        """
        self.welcome_page.search_click(WelcomePageLocators.QUERY_IMAGE_LOOP)
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)

        assert self.driver.current_url == "https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the" \
                                          "-internet/", \
            "URL должен быть https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/"

    @allure.title('Основная страница. Нажатие на картинку с письмом')
    @pytest.mark.UI
    def test_welcome_page_click_on_image_smtp(self):
        """
          Тестирование: Основная страница. Нажатие на картинку с письмом
          Предусловия: Пользователь авторизован
          Шаги:
          1. Нажать на картинку с письмом
          Ожидаемый результат:
          1. Пользователя редирекнет (новая вкладка) на
          https://ru.wikipedia.org/wiki/SMTP (+)
          Фактический результат:
          1. Пользователя редирекнет (новая вкладка) на
          https://ru.wikipedia.org/wiki/SMTP
        """
        self.welcome_page.search_click(WelcomePageLocators.QUERY_IMAGE_SMTP)
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)

        assert self.driver.current_url == "https://ru.wikipedia.org/wiki/SMTP", \
            "URL должен быть https://ru.wikipedia.org/wiki/SMTP"

    @allure.title('Основная страница. Сравнить отображаемый текст Logged as.. с реальным положеним')
    @pytest.mark.UI
    def test_welcome_page_logged_as_text(self):
        """
          Тестирование: Основная страница. Сравнить отображаемый текст Logged as.. с реальным положеним
          Предусловия: Пользователь авторизован
          Шаги:
          1. Через UI посмотреть пользователя, указанного в предложении Logged as ...
          Ожидаемый результат:
          1. Будет отображена надпись 'Logged as {username}', где username -  username текущего пользователя (+)
          Фактический результат:
          1. Отображается надпись 'Logged as {username}', где username -  username текущего пользователя
        """
        assert self.welcome_page.find(WelcomePageLocators.QUERY_LOGGED_AS).text == f"Logged as {USERNAME}", \
            f"Должно отображаться: Logged as {USERNAME}"
        assert self.driver.current_url == self.welcome_page.url, f"URL должен быть http://{APP_HOST}:{APP_PORT}/welcome/"

    @allure.title('Основная страница. Сравнить отображаемый текст User.. с реальным положеним')
    @pytest.mark.UI
    def test_welcome_page_user_text(self):
        """
          Тестирование: Основная страница. Сравнить отображаемый текст User с реальным положеним
          Предусловия: Пользователь авторизован
          Шаги:
          1. Через UI посмотреть данные пользователя, указанные в User: {name} {surname}
          Ожидаемый результат:
          1. Будет отображена надпись 'User: {name} {surname}}', где name -  name текущего пользователя, surname - фамилия
          текущего пользователя (+)
          Фактический результат:
          1. Отображается надпись 'User: {name} {surname}}', где name -  name текущего пользователя, surname - фамилия
          текущего пользователя
        """
        user_db = self.mysql.session.query(Users).filter_by(username=USERNAME).first()
        name = user_db.name
        surname = user_db.surname

        assert self.welcome_page.find(WelcomePageLocators.QUERY_USER).text == f"User: {name} {surname}", \
            f"Должно отображаться: User: {name} {surname}"
        assert self.driver.current_url == self.welcome_page.url, f"URL должен быть http://{APP_HOST}:{APP_PORT}/welcome/"

    @allure.title('Основная страница. Сравнить отображаемый VK_ID с реальным положеним')
    @pytest.mark.UI
    def test_welcome_page_vk_id_text(self):
        """
          Тестирование: Основная страница. Сравнить отображаемый VK_ID с реальным положеним
          Предусловия: Пользователь авторизован
          Шаги:
          1. Через UI посмотреть содержимое в VK_ID: ...
          Ожидаемый результат:
          1. Будет отображена надпись VK_ID: 10 рандомных цифр (+)
          Фактический результат:
          1. Будет отображена надпись VK_ID: 10 рандомных цифр
        """
        VK_ID = self.welcome_page.find(WelcomePageLocators.QUERY_VK_ID).text.split(" ")[-1]
        assert re.match("\d{10}", VK_ID)
        assert self.driver.current_url == self.welcome_page.url, f"URL должен быть http://{APP_HOST}:{APP_PORT}/welcome/"

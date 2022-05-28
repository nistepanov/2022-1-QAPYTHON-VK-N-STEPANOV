import logging
import os
import shutil
import sys

import allure
import pytest

from final_project.code.mysql.client import MySqlClient
from final_project.code.settings.config import *

def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default=f'http://{APP_HOST}:{APP_PORT}/')
    parser.addoption('--debug_log', action='store_true')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\test'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir
    config.mysql_client = MySqlClient()


@pytest.fixture(scope='function')
def mysql_client_fixture():
    with allure.step("Выполняем коннект к БД и возвращаем объект соединения"):
        mysql_client = MySqlClient()
        mysql_client.connect()
    yield mysql_client
    with allure.step("Закрываем соединение с БД"):
        mysql_client.connection.close()


@pytest.fixture(scope='session')
@allure.step("Определяем путь директории для логов в зависимости от ОС")
def base_temp_dir():
    if sys.platform.startswith('win'):
        base_dir = 'C:\\test'
    else:
        base_dir = '/tmp/tests'
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    return base_dir


@pytest.fixture(scope='function')
@allure.step("Создаем директорию для логов")
def temp_dir(request, base_temp_dir):
    test_dir = os.path.join(request.config.base_temp_dir, request._pyfuncitem.nodeid)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
@allure.step("Инициализация логгера")
def logger(temp_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.DEBUG

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()


@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')
    debug_log = request.config.getoption('--debug_log')
    if request.config.getoption('--selenoid'):
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
        selenoid = 'http://selenoid_hub:4444/wd/hub'
    else:
        selenoid = None
        vnc = False

    return {
        'url': url,
        'browser': browser,
        'debug_log': debug_log,
        'selenoid': selenoid,
        'vnc': vnc,
    }

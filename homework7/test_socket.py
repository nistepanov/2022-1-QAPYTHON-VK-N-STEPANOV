import json
import socket
import time

import requests
from faker.proxy import Faker

from server import settings

url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'
fake = Faker()


def test_get_surname_positive():
    rand_name = fake.name().split(" ")[0]
    rand_surname = fake.name().split(" ")[1]
    requests.post(f'{url}/add_user', json={'name': f'{rand_name}', f'surname': rand_surname})

    target_host = settings.MOCK_HOST
    target_port = int(settings.MOCK_PORT)

    endpoint = f'/get_surname/{rand_name}'
    data = f"?surname={rand_surname}"
    full_req = endpoint + data
    # создаём объект клиентского сокета
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # выставляем ожидание для сокета
    client.settimeout(0.1)

    # устанавливаем соединение
    client.connect((target_host, target_port))

    # создаем и выполняем запрос
    request = f'GET {full_req} HTTP/1.1\r\nHost:{target_host}\r\n\r\n'
    client.sendall(request.encode())

    total_data = []
    start = time.time()
    try:
        while time.time() - start < 15:
            # читаем данные из сокета до тех пор пока они там есть
            data = client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                break
    finally:
        pass

    data = ''.join(total_data).splitlines()
    response_code = int(data[0].split(' ')[1])
    response_message = data[0].split(' ')[2]
    print(data)
    client.close()

    assert json.loads(data[-1]) == rand_surname
    assert response_code == 200
    assert response_message == 'OK'


def test_get_surname_negative():
    rand_name = fake.name().split(" ")[0]

    requests.post(f'{url}/add_user', json={'name': f'{rand_name}'})

    target_host = settings.MOCK_HOST
    target_port = int(settings.MOCK_PORT)

    endpoint = f'/get_surname/{rand_name}'

    # создаём объект клиентского сокета
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # выставляем ожидание для сокета
    client.settimeout(0.1)

    # устанавливаем соединение
    client.connect((target_host, target_port))

    # создаем и выполняем запрос
    request = f'GET {endpoint} HTTP/1.1\r\nHost:{target_host}\r\n\r\n'
    client.send(request.encode())

    total_data = []
    start = time.time()
    try:
        while time.time() - start < 15:
            # читаем данные из сокета до тех пор пока они там есть
            data = client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                break
    finally:
        pass

    data = ''.join(total_data).splitlines()
    response_code = int(data[0].split(' ')[1])
    response_message = data[0].split(' ')[2] + " " + data[0].split(' ')[3]

    client.close()

    print(data)

    assert json.loads(data[-1]) == f'Surname for user "{rand_name}" not found'
    assert response_message == "NOT FOUND"
    assert response_code == 404


def test_put_surname_positive():
    rand_name = fake.name().split(" ")[0]
    rand_surname = fake.name().split(" ")[1]

    requests.post(f'{url}/add_user', json={'name': f'{rand_name}', 'surname': f'{rand_surname}'})

    target_host = settings.MOCK_HOST
    target_port = int(settings.MOCK_PORT)

    params = f'/update_surname/{rand_surname}'

    # создаём объект клиентского сокета
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # выставляем ожидание для сокета
    client.settimeout(0.1)

    # устанавливаем соединение
    client.connect((target_host, target_port))

    # создаем и выполняем запрос

    request = f'PUT {params} HTTP/1.1\r\nHost:{target_host}\r\n\r\n'
    client.send(request.encode())

    total_data = []
    start = time.time()
    try:
        while time.time() - start < 15:
            # читаем данные из сокета до тех пор пока они там есть
            data = client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                break
    finally:
        pass

    data = ''.join(total_data).splitlines()
    response_code = int(data[0].split(' ')[1])
    response_message = data[0].split(' ')[2]

    client.close()

    assert json.loads(data[-1]) != rand_surname
    assert response_code == 200
    assert response_message == 'OK'


def test_put_surname_negative():
    rand_name = fake.name().split(" ")[0]
    requests.post(f'{url}/add_user', json={'name': f'{rand_name}'})

    target_host = settings.MOCK_HOST
    target_port = int(settings.MOCK_PORT)
    endpoint = f'/update_surname/{None}'

    # создаём объект клиентского сокета
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # выставляем ожидание для сокета
    client.settimeout(0.1)

    # устанавливаем соединение
    client.connect((target_host, target_port))

    # создаем и выполняем запрос

    request = f'PUT {endpoint} HTTP/1.1\r\nHost:{target_host}\r\n\r\n'
    client.send(request.encode())

    total_data = []
    start = time.time()
    try:
        while time.time() - start < 15:
            # читаем данные из сокета до тех пор пока они там есть
            data = client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                break
    finally:
        pass

    data = ''.join(total_data).splitlines()
    print(data)

    response_code = int(data[0].split(' ')[1])
    response_message = data[0].split(' ')[2] + " " + data[0].split(' ')[3]

    client.close()

    assert data[-1] == '"Cannot update surname, because Surname is None!"'
    assert response_message == "NOT FOUND"
    assert response_code == 404


def test_delete_surname_positive():
    rand_name = fake.name().split(" ")[0]
    rand_surname = fake.name().split(" ")[1]

    requests.post(f'{url}/add_user', json={'name': f'{rand_name}', 'surname': f'{rand_surname}'})

    target_host = settings.MOCK_HOST
    target_port = int(settings.MOCK_PORT)

    endpoint = f'/delete_surname/{rand_surname}'

    # создаём объект клиентского сокета
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # выставляем ожидание для сокета
    client.settimeout(0.1)

    # устанавливаем соединение
    client.connect((target_host, target_port))

    # создаем и выполняем запрос

    request = f'DELETE {endpoint} HTTP/1.1\r\nHost:{target_host}\r\n\r\n'
    client.send(request.encode())

    total_data = []
    start = time.time()
    try:
        while time.time() - start < 15:
            # читаем данные из сокета до тех пор пока они там есть
            data = client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                break
    finally:
        pass

    data = ''.join(total_data).splitlines()
    response_code = int(data[0].split(' ')[1])
    response_message = data[0].split(' ')[2]

    client.close()

    assert json.loads(data[-1])['surname'] == ""
    assert response_code == 200
    assert response_message == 'OK'


def test_delete_surname_negative():
    rand_name = fake.name().split(" ")[0]
    requests.post(f'{url}/add_user', json={'name': f'{rand_name}'})

    target_host = settings.MOCK_HOST
    target_port = int(settings.MOCK_PORT)
    endpoint = f'/delete_surname/{None}'

    # создаём объект клиентского сокета
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # выставляем ожидание для сокета
    client.settimeout(0.1)

    # устанавливаем соединение
    client.connect((target_host, target_port))

    # создаем и выполняем запрос

    request = f'DELETE {endpoint} HTTP/1.1\r\nHost:{target_host}\r\n\r\n'
    client.send(request.encode())

    total_data = []
    start = time.time()
    try:
        while time.time() - start < 15:
            # читаем данные из сокета до тех пор пока они там есть
            data = client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                break
    finally:
        pass

    data = ''.join(total_data).splitlines()
    print(data)

    response_code = int(data[0].split(' ')[1])
    response_message = data[0].split(' ')[2] + " " + data[0].split(' ')[3]

    client.close()

    assert data[-1] == '"Cannot delete surname, because user has not surname!"'
    assert response_message == "NOT FOUND"
    assert response_code == 404

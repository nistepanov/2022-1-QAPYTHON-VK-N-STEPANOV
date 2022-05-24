import requests
from faker.proxy import Faker

from server import settings

url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'


def test_add_get_user():
    fake = Faker()
    rand_name = fake.name().split(" ")[0]

    resp = requests.post(f'{url}/add_user', json={'name': f'{rand_name}'})
    user_id_from_add = resp.json()['user_id']

    resp = requests.get(f'{url}/get_user/{rand_name}')
    user_id_from_get = resp.json()['user_id']

    assert user_id_from_add == user_id_from_get


def test_add_existent_user():
    requests.post(f'{url}/add_user', json={'name': 'Vasya'})
    resp = requests.post(f'{url}/add_user', json={'name': 'Vasya'})

    assert resp.status_code == 400


def test_get_non_existent_user():
    resp = requests.get(f'{url}/Masha')

    assert resp.status_code == 404


def test_with_age():
    requests.post(f'{url}/add_user', json={'name': 'Stepan'})

    resp = requests.get(f'{url}/get_user/Stepan')
    age = resp.json()['age']

    assert isinstance(age, int)
    assert 0 <= age <= 100


def test_has_surname():
    fake = Faker()
    rand_name = fake.name().split(" ")[0]
    rand_surname = fake.name().split(" ")[1]

    resp_post = requests.post(f'{url}/add_user', json={'name': f'{rand_name}', 'surname': f'{rand_surname}'})

    if resp_post.status_code == 201:
        resp_get = requests.get(f'{url}/get_user/{rand_name}')
        surname = resp_get.json()['surname']

        assert surname == rand_surname

    else:
        raise AssertionError("Failed with creating user")


def test_has_no_surname():
    requests.post(f'{url}/add_user', json={'name': 'Sveta'})

    resp = requests.get(f'{url}/get_user/Sveta')
    surname = resp.json()['surname']

    assert surname is None

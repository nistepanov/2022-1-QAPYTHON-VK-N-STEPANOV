import logging
import random
import string

from faker.proxy import Faker
from flask import Flask, jsonify, request

VK_API_HOST = '0.0.0.0'
VK_API_PORT = 8787

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
url = f'http://{VK_API_HOST}:{VK_API_PORT}'

logging.basicConfig(filename='/tmp/mock_stdout', level=logging.INFO, filemode='w')
fake = Faker()


class Randomizer:
    @staticmethod
    def generate_random_vk_id():
        letters = string.digits
        rand_vk_id = ''.join(random.sample(letters, 10))
        return rand_vk_id


def logging_http_methods_info(http_entity, type_http='response'):
    if type_http == 'request':
        logging.info('Additional request information:\n')
        logging.info(http_entity.headers)
    else:
        logging.info('Additional response information:\n')
        logging.info(http_entity)


class FlaskMock:
    @staticmethod
    @app.route('/vk_id/<name>', methods=['GET'])
    def get_user_surname(name):
        if name != 'None':
            logging_http_methods_info(request, 'request')
            vk_id = Randomizer.generate_random_vk_id()

            return jsonify({'vk_id': vk_id}), 200
        else:
            logging_http_methods_info("Not found")

            return jsonify("Not found"), 404


if __name__ == '__main__':
    app.run(VK_API_HOST, VK_API_PORT)

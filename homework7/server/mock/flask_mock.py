import logging
import os
import threading

from faker.proxy import Faker
from flask import Flask, jsonify, request

from server import settings

app = Flask(__name__)
logging.basicConfig(filename='/tmp/mock_stdout', level=logging.INFO, filemode='w')
fake = Faker()


def logging_http_methods_info(http_entity, type_http='response'):
    if type_http == 'request':
        logging.info('Additional request information:\n')
        logging.info(http_entity.headers)
    else:
        logging.info('Additional response information:\n')
        logging.info(http_entity)


class FlaskMock:
    @staticmethod
    @app.route('/get_surname/<name>', methods=['GET'])
    def get_user_surname(name):
        logging_http_methods_info(request, 'request')
        surname = request.args.get('surname')
        if name is not None and surname is not None:
            logging_http_methods_info(jsonify(surname))
            return jsonify(surname), 200
        else:
            logging_http_methods_info(f'Surname for user "{name}" not found')
            return jsonify(f'Surname for user "{name}" not found'), 404

    @staticmethod
    @app.route('/update_surname/<surname>', methods=['PUT'])
    def update_user_surname(surname):
        logging_http_methods_info(request, 'request')

        if surname != 'None':
            new_surname = fake.name().split(" ")[1]
            logging_http_methods_info(jsonify(new_surname))
            return jsonify({'surname': new_surname}), 200
        else:
            logging_http_methods_info(f'Cannot update surname, because Surname is None!')
            return jsonify(f'Cannot update surname, because Surname is None!'), 404

    @staticmethod
    @app.route('/delete_surname/<surname>', methods=['DELETE'])
    def delete_user_surname(surname):
        logging_http_methods_info(request, 'request')

        if surname != 'None':
            new_surname = ""
            logging_http_methods_info(jsonify(new_surname))
            return jsonify({'surname': new_surname}), 200
        else:
            logging_http_methods_info(f'Cannot delete surname, because user has not surname!')
            return jsonify(f'Cannot delete surname, because user has not surname!'), 404

    @staticmethod
    @app.route('/shutdown', methods=['GET'])
    def shutdown():
        AuxiliaryMethods.shutdown_mock()
        return jsonify(f'Ok, exiting'), 200


class AuxiliaryMethods:
    @staticmethod
    def run_mock():
        server = threading.Thread(target=app.run, kwargs={
            'host': settings.MOCK_HOST,
            'port': settings.MOCK_PORT
        })

        server.start()
        return server

    @staticmethod
    def shutdown_mock():
        # os.kill(os.getppid(), signal.SIGTERM)
        terminate_func = request.environ.get('werkzeug.server.shutdown')
        if terminate_func:
            terminate_func()


if __name__ == '__main__':
    host = os.environ.get('MOCK_HOST', '127.0.0.1')
    port = os.environ.get('MOCK_PORT', '8083')

    app.run(host, port)

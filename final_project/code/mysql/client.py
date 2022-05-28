import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from final_project.code.settings.config import *


class MySqlClient:

    def __init__(self):
        self.user = 'test_qa'
        self.port = MYSQL_PORT
        # self.port = 3306
        self.password = 'qa_test'
        self.host = MYSQL_HOST
        # self.host = '0.0.0.0'
        self.db_name = MYSQL_DB
        # self.db_name = 'vkeducation'

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self):
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

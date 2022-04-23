import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from mysql.utils.models import Base


class MySqlClient:

    def __init__(self, db_name, user, password):
        self.user = user
        self.port = 3306
        self.password = password
        self.host = '127.0.0.1'
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def create_db(self):
        self.connect(db_created=False)
        self.connection.execute(f'CREATE database if not exists {self.db_name}')
        self.connection.close()

    def drop_db(self):
        self.connect(db_created=False)
        self.connection.execute(f'DROP database {self.db_name}')
        self.connection.close()

    def create_count_requests(self):
        if not inspect(self.engine).has_table('count_requests'):
            Base.metadata.tables['count_requests'].create(self.engine)

    def create_count_requests_type(self):
        if not inspect(self.engine).has_table('count_requests_type'):
            Base.metadata.tables['count_requests_type'].create(self.engine)

    def create_count_top_resources(self):
        if not inspect(self.engine).has_table('count_top_resources'):
            Base.metadata.tables['count_top_resources'].create(self.engine)

    def create_server_errors_requests(self):
        if not inspect(self.engine).has_table('count_requests_server_error'):
            Base.metadata.tables['count_requests_server_error'].create(self.engine)

    def create_client_error_requests(self):
        if not inspect(self.engine).has_table('count_requests_client_error'):
            Base.metadata.tables['count_requests_client_error'].create(self.engine)

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CountRequests(Base):
    __tablename__ = 'count_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"(" \
               f"id='{self.id}'," \
               f"count:'{self.count}'" \
               f""

    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer, nullable=True)


class CountRequestsType(Base):
    __tablename__ = 'count_requests_type'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"" \
               f"id='{self.id}'," \
               f"type='{self.type}', " \
               f"count:'{self.count}' " \
               f""

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(10), nullable=True)
    count = Column(Integer, nullable=True)


class CountTopResources(Base):
    __tablename__ = 'count_top_resources'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"" \
               f"id='{self.id}'," \
               f"path='{self.path}', " \
               f"count='{self.count}' " \
               f""

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(200), nullable=True)
    count = Column(Integer, nullable=True)


class CountTopSizeRequestsClientError(Base):
    __tablename__ = 'count_requests_client_error'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"" \
               f"id:'{self.id}'," \
               f"path:'{self.path}', " \
               f"ip:'{self.ip}'," \
               f"size:'{self.size}'," \
               f"code:'{self.code}" \
               f""

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(500), nullable=True)
    size = Column(Integer, nullable=True)
    code = Column(Integer, nullable=True)
    ip = Column(String(200), nullable=True)


class CountTopFrequencyRequestsServerError(Base):
    __tablename__ = 'count_requests_server_error'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"" \
               f"id:'{self.id}'," \
               f"frequency:'{self.frequency}'," \
               f"ip:'{self.ip}'" \
               f""

    id = Column(Integer, primary_key=True, autoincrement=True)
    frequency = Column(Integer, nullable=True)
    ip = Column(String(200), nullable=True)

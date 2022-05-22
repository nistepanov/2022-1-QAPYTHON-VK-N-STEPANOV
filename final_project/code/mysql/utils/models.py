import allure

from sqlalchemy import Column, Integer, VARCHAR, DateTime, SMALLINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<test_users(id='{self.id}'," \
               f"username='{self.username}'," \
               f"name='{self.name}'," \
               f"surname='{self.surname}'," \
               f"surname='{self.middle_name}'," \
               f"password='{self.password}'," \
               f"email='{self.email}'," \
               f"access='{self.access}'," \
               f"active='{self.active}'," \
               f"start_active_time='{self.start_active_time}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), default=None)
    surname = Column(VARCHAR(255), default=None)
    middle_name = Column(VARCHAR(255), default=None)
    username = Column(VARCHAR(16), default=None)
    password = Column(VARCHAR(255), default=None)
    email = Column(VARCHAR(64), default=None)
    access = Column(SMALLINT, default=None)
    active = Column(SMALLINT, default=None)
    start_active_time = Column(DateTime, default=None)

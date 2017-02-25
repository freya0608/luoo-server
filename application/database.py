from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:""@localhost/luoo?charset=utf8")

Base = declarative_base()

Session = sessionmaker(bind=engine)


class BaseSession:
    session = None

    def close(self):
        pass

    def __new__(cls):
        if cls.session is None:
            cls.session = Session()
            return cls.session
        else:
            pass

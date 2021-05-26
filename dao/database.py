import os

import yaml
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from extra.to_dict import ToDict

Base = declarative_base()


class Review(Base, ToDict):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(100))
    professor_id = Column(Integer, ForeignKey('professor.id'))
    course = Column(String(100))
    score = Column(Integer)
    difficulty = Column(Integer)


class Professor(Base, ToDict):
    __tablename__ = 'professor'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    score = Column(Integer)
    difficulty = Column(Integer)
    reviews = relationship('Review', backref='professor')


class DatabaseConecctionData:
    def __init__(self, user, password, host, databasename, driver):
        self.user = user
        self.password = password
        self.host = host
        self.databasename = databasename
        self.driver = driver


class DatabaseConnection:
    def __init__(self, settings="database.yaml"):
        self.settings = settings

    def get_session_for_database_created(self):
        databaseDataConection = self.load_settings(self.settings)

        engine = create_engine(
            f'{databaseDataConection.driver}:///'
            f'{databaseDataConection.databasename}.{databaseDataConection.driver}'
        )

        session = sessionmaker()
        session.configure(bind=engine)
        return session()

    def create_database(self):
        databaseDataConection = self.load_settings(self.settings)

        engine = create_engine(
            f'{databaseDataConection.driver}:///'
            f'{databaseDataConection.databasename}.{databaseDataConection.driver}'
        )

        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(engine)

    def load_settings(self, settings):
        if os.path.exists(settings):
            settings_file = open('database.yaml')
            data = yaml.load(settings_file, Loader=yaml.FullLoader)
            settings_file.close()
            return DatabaseConecctionData(
                data["conection"]["user"],
                data["conection"]["password"],
                data["conection"]["host"],
                data["conection"]["database"],
                data["conection"]["driver"]
            )
        else:
            raise Exception(f"{settings} file does not exists")

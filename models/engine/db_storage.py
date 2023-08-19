#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """SQL database storage"""
    __engine__ = None
    __session__ = None

    def __init__(self):
        """Create engine and connect to database"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV", "none")

        self.__engine__ = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine__)

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session__.query(cls)
            for items in query:
                key = "{}.{}".format(type(items).__name__, items.id)
                dic[key] = items
        else:
            listArray = [State, City, User, Place, Review, Amenity]
            for lists in listArray:
                query = self.__session__.query(lists)
                for items in query:
                    key = "{}.{}".format(type(items).__name__, items.id)
                    dic[key] = items
        return (dic)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session__.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session__.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session__.delete(obj)

    def reload(self):
        """Create current database session from the engine
        using a sessionmaker"""
        self.__session__ = Base.metadata.create_all(self.__engine__)
        sessions = sessionmaker(bind=self.__engine__, expire_on_commit=False)
        Session = scoped_session(sections)
        self.__session__ = Session()

    def close(self):
        """Remove session"""
        self.__session__.close()

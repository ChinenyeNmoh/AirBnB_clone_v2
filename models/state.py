#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
import models
from models.city import City
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City",
                          backref="state", cascade="all, delete,delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def cities(self):
            """ returns list of City instances related to state """
            from models import storage
            list_cities = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    list_cities.append(city)
            return list_cities

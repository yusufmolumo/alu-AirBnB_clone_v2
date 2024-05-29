#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)


if getenv('HBNB_TYPE_STORAGE') == 'db':
    cities = relationship('City', backref='state',
                          cascade='all, delete-orphan')

else:
    @property
    def cities(self):
        """Getter for cities"""
        cities_list = []
        for city in models.storage.all(City).values():
            if city.state_id == self.id:
                cities_list.append(city)
        return cities_list

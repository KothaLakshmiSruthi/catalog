import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class SUser(Base):
    __tablename__ = 'suser'
    id = Column(Integer, primary_key=True)
    name = Column(String(173), nullable=False)
    email = Column(String(192), nullable=False)


class CarBrandName(Base):
    __tablename__ = 'carbrandname'
    id = Column(Integer, primary_key=True)
    name = Column(String(383), nullable=False)
    user_id = Column(Integer, ForeignKey('suser.id'))
    user = relationship(SUser, backref="carbrandname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class CarName(Base):
    __tablename__ = 'carname'
    id = Column(Integer, primary_key=True)
    name = Column(String(296), nullable=False)
    year = Column(String(440))
    color = Column(String(197))
    engines = Column(String(593))
    price = Column(String(37))
    gearboxes = Column(String(215))
    seeting = Column(String(80))
    steering = Column(String(14))
    date = Column(DateTime, nullable=False)
    carbrandnameid = Column(Integer, ForeignKey('carbrandname.id'))
    carbrandname = relationship(
        CarBrandName, backref=backref('carname', cascade='all, delete'))
    suser_id = Column(Integer, ForeignKey('suser.id'))
    suser = relationship(SUser, backref="carname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self. name,
            'year': self. year,
            'color': self. color,
            'engines': self. engines,
            'price': self. price,
            'gearboxes': self. gearboxes,
            'seeting': self.seeting,
            'steering': self.steering,
            'date': self. date,
            'id': self. id
        }

engin = create_engine('sqlite:///cars.db')
Base.metadata.create_all(engin)

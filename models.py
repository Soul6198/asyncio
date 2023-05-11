from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class People(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    birth_year = Column(Integer, nullable=False)
    eye_color = Column(Integer, nullable=False)
    films = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    hair_color = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    homeworld = Column(Integer, nullable=False)
    mass = Column(Integer, nullable=False)
    name = Column(Integer, nullable=False)
    skin_color = Column(Integer, nullable=False)
    species = Column(Integer, nullable=True)
    starships = Column(Integer, nullable=True)
    vehicles = Column(Integer, nullable=True)

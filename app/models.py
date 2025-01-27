from sqlalchemy import Column, Integer, String, Float , TIMESTAMP, func
from .dbase_api import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    cardnumber = Column(String, nullable=False)
    month_year = Column(String, nullable=True)
    cvc = Column(String, nullable=True)
    cardholder = Column(String, nullable=True)

class Purch(Base):
    __tablename__ = "purchase"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    productid = Column(String, nullable=False)
    totality = Column(String, nullable=True)
    number = Column(String, nullable=True)

class Store(Base):
    __tablename__ = "store"
    productid = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    prodname = Column(String, nullable=False)
    instock = Column(Integer, nullable=True)
    prize = Column(Float, nullable=True)
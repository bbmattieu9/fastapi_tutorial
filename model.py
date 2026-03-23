from sqlalchemy import Column, Integer, VARCHAR
from database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(255))
    author = Column(VARCHAR(255))
    publish_date = Column(VARCHAR(255))


# class User(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(VARCHAR(255))
#     first_name = Column(VARCHAR(255))
#     last_name = Column(VARCHAR(255))
#     password = Column(VARCHAR(255))

from sqlalchemy import Column, Integer, String, DateTime
from auth_database import Base

class User(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True, unique=True, nullable=False)
    email = Column(String(255), index=True, unique=True, nullable=False)
    hashed_password = Column(String(255))
    role = Column(String(50), default='user')
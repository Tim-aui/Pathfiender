from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy import Column, String, Integer, Date, ARRAY, Text, ForeignKey # type: ignore

Base = declarative_base()

class Users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    role = Column(ARRAY(String(255)))
    create_at = Column(Date()) 
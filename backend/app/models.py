from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy import Column, String, Integer, Date, ARRAY, Text, ForeignKey, Boolean

Base = declarative_base()

class Users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    active = Column(Boolean(True))
    role = Column(ARRAY(String(255)))
    create_at = Column(Date()) 

class Products(Base):
    __tablename__ = "products"

    id = Column(String(255), unique=True, nullable=False)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(Text(), unique=True, nullable= False)
    #creator_id = 
    create_at = Column(Date())
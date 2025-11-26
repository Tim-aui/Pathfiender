# models_simple.py
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from config.database import engine
Base = declarative_base()
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    active = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.utcnow)

    products = relationship("Product", backref="creator")





class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    slug = Column(String(255))
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    create_at = Column(DateTime, default=datetime.utcnow())

    parent = relationship("Category", remote_side=[id], backref="subcategories")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    create_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", backref="products")
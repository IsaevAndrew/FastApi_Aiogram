from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    artikul = Column(Integer, primary_key=True, index=True, unique=True,
                     nullable=False)  # Артикул товара
    name = Column(String, nullable=False)  # Название товара
    price = Column(Float, nullable=False)  # Цена
    rating = Column(Float, nullable=False)  # Рейтинг
    stock = Column(Integer,
                   nullable=False)  # Суммарное количество товара на всех складах
    updated_at = Column(TIMESTAMP, server_default=func.now(),
                        onupdate=func.now())  # Время обновления записи


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    artikul = Column(Integer, unique=True,
                     nullable=False)  # Уникальный артикул товара
    created_at = Column(TIMESTAMP,
                        server_default=func.now())  # Время создания подписки


class ProductRequest(BaseModel):
    artikul: int = Field()

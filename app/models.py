from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Brand(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String(50), unique=True, nullable=False)

    models = relationship("Model", back_populates="brand", cascade="all, delete")


class Model(Base):
    __tablename__ = "models"

    model_id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(50), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.brand_id", ondelete="CASCADE"), nullable=False)

    brand = relationship("Brand", back_populates="models")
    cars = relationship("Car", back_populates="model", cascade="all, delete")


class Color(Base):
    __tablename__ = "colors"

    color_id = Column(Integer, primary_key=True, index=True)
    color_name = Column(String(30), nullable=False, unique=True)

    cars = relationship("Car", back_populates="color", cascade="all, delete")


class Car(Base):
    __tablename__ = "cars"

    car_id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.model_id", ondelete="CASCADE"), nullable=False)
    color_id = Column(Integer, ForeignKey("colors.color_id", ondelete="CASCADE"), nullable=False)
    purchased_date = Column(Date, nullable=False)

    model = relationship("Model", back_populates="cars")
    color = relationship("Color", back_populates="cars")

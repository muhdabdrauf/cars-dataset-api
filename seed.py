import os 
import pandas as pd 
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine, Column, Integer, String, Date, ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CSV_PATH = os.getenv("CSV_PATH")
Base = declarative_base()

class Brand(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(String(50), unique=True, nullable=False)

    models = relationship("Model", back_populates="brand", cascade="all, delete-orphan")

class Model(Base):
    __tablename__ = "models"

    model_id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(50), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.brand_id", ondelete="CASCADE"), nullable=False)

    brand = relationship("Brand", back_populates="models")
    cars = relationship("Car", back_populates="model", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("model_name", "brand_id", name="uq_model_brand"),
        Index("idx_models_brand_id", "brand_id"),
    )

class Color(Base):
    __tablename__ = "colors"

    color_id = Column(Integer, primary_key=True, autoincrement=True)
    color_name = Column(String(30), unique=True, nullable=False)

    cars = relationship("Car", back_populates="color", cascade="all, delete-orphan")

class Car(Base):
    __tablename__ = "cars"

    car_id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("models.model_id", ondelete="CASCADE"), nullable=False)
    color_id = Column(Integer, ForeignKey("colors.color_id", ondelete="CASCADE"), nullable=False)
    purchased_date = Column(Date, nullable=False)

    model = relationship("Model", back_populates="cars")
    color = relationship("Color", back_populates="cars")

    __table_args__ = (
        Index("idx_cars_model_id", "model_id"),
        Index("idx_cars_color_id", "color_id"),
    )

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def seed_from_csv(CSV_PATH):
    df = pd.read_csv(CSV_PATH)

    try:
        for _, row in df.iterrows():
            car_id = int(row["id"]) 
            brand_name = row["car_brand"].strip()
            model_name = row["car_model"].strip()
            color_name = row["car_color"].strip()
            purchased_date = pd.to_datetime(row["purchased_date"]).date()

            brand = session.query(Brand).filter_by(brand_name=brand_name).first()
            if not brand:
                brand = Brand(brand_name=brand_name)
                session.add(brand)
                session.flush()  

            model = (
                session.query(Model)
                .filter_by(model_name=model_name, brand_id=brand.brand_id)
                .first()
            )
            if not model:
                model = Model(model_name=model_name, brand_id=brand.brand_id)
                session.add(model)
                session.flush()  

            color = session.query(Color).filter_by(color_name=color_name).first()
            if not color:
                color = Color(color_name=color_name)
                session.add(color)
                session.flush()  

            existing_car = session.query(Car).filter_by(car_id=car_id).first()
            if not existing_car:
                car = Car(
                    car_id=car_id,
                    model_id=model.model_id,
                    color_id=color.color_id,
                    purchased_date=purchased_date,
                )
                session.add(car)

        session.commit()
        print("✅ Seeding completed successfully!")

    except Exception as e:
        session.rollback()
        print("❌ Error during seeding:", e)

    finally:
        session.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    seed_from_csv(CSV_PATH)
        
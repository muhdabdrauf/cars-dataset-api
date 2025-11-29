import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine - connects SQLAlchemy to prosgreSQL
engine = create_engine(DATABASE_URL, echo=True)

# Session factory - used by FastAPI routes to access the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models - your models will inherit from this 
Base = declarative_base()

# Dependency to get DB session - a reusable dependecy to open/close sessions automatically in routes
def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
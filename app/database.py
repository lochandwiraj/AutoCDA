# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://autocda:autocda@localhost:5432/autocda")

# Use SQLAlchemy synchronous engine (simple for Day1)
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def init_db():
    from app import models
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized!")

import os
import datetime as dt
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Railway ka DATABASE_URL variable uthayega, nahi milega toh local SQLite chalayega
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./skyfly_leads.db")

# PostgreSQL ke liye simple engine, SQLite ke liye thread check false
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    service_interested = Column(String)
    contact_info = Column(String)
    budget = Column(String, nullable=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

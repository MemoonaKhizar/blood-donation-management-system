from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./smart_donation.db"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # Required for SQLite
)

# Create a session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

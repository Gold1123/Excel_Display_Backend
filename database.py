from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/excel"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def clear_database():
    # Use the Base metadata to drop all 
    print("clear database")
    Base.metadata.drop_all(bind=engine)

    # Optionally, you can also recreate the tables after dropping them
    Base.metadata.create_all(bind=engine)
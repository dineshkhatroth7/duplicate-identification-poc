from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "postgresql://postgres:Dinesh%40123@localhost:5432/duplicate_poc"

try:

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )

except SQLAlchemyError as e:

    raise Exception(f"Database connection failed: {str(e)}")


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
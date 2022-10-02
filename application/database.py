from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pydantic import PostgresDsn


from application import settings


SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
    scheme="postgresql",
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    path=f"/{settings.DB_NAME or ''}",
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # TODO по хорошему делать это руками где надо, а не всегда
        db.commit()
        db.close()

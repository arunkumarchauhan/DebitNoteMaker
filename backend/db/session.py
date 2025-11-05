from sqlalchemy import create_engine, event
# from sqlalchemy.ext.declarative import declarative_base
from core.config import settings
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, declarative_base
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL
# SQLALCHEMY_DATABASE_URL= "sqlite:///./sql_app.db"
print("Datebase url is ",SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool, connect_args={"check_same_thread": False})


@event.listens_for(engine, "connect")
def _enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()

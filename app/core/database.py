from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings


DATABASE_URL = URL.create(
    drivername='postgresql+psycopg2',
    host=settings.db_host,
    port=settings.db_port,
    username=settings.db_user,
    password=settings.db_pass,
    database=settings.db_name,
)
engine = create_engine(url=DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
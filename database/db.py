from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Settings

settings = Settings()

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@' \
                          f'{settings.db_host}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

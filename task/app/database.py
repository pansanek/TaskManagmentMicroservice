from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from task.app.settings import settings


engine = create_engine(settings.postgres_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

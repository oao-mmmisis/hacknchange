from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "postgresql://test:test@postgres/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)

def get_db() -> Generator[Session, None, None]:
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
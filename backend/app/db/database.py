from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# The Engine knows how to connect to PostgreSQL
engine = create_engine(
    settings.database_url,
    echo=True,  # Show SQL queries in the terminal (great for learning)
)

# Creates database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
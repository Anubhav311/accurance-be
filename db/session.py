from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,   # important for Neon
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

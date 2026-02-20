from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# DATABASE_URL set → use PostgreSQL (Vercel Postgres, Supabase, etc.)
# Otherwise fall back to local SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Vercel Postgres uses postgres:// — SQLAlchemy needs postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,        # auto-reconnect if connection drops
        pool_size=5,
        max_overflow=2,
    )
else:
    # Local SQLite (development only)
    LOCAL_DB = "sqlite:///./tournament.db"
    engine = create_engine(
        LOCAL_DB,
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

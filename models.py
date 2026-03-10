import os
import re
from sqlalchemy import Column, String, DateTime, JSON, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import uuid

# Resolve DATABASE URL with required transformations
_db_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or "sqlite:///./app.db"
if _db_url.startswith("postgresql+asyncpg://"):
    _db_url = _db_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
elif _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql+psycopg://")

# Add SSL args for non‑local PostgreSQL connections
connect_args = {}
if not _db_url.startswith("sqlite") and "localhost" not in _db_url and "127.0.0.1" not in _db_url:
    connect_args["sslmode"] = "require"

engine = create_engine(_db_url, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

TABLE_PREFIX = "ls_"

class Bookmark(Base):
    __tablename__ = f"{TABLE_PREFIX}bookmarks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String, nullable=False)
    title = Column(String, nullable=True)
    summary_short = Column(String, nullable=True)
    summary_long = Column(String, nullable=True)
    tags = Column(JSON, nullable=False, default=list)  # stored as JSON array
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

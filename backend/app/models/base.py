"""
Base model with common fields for all models.
"""
from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.ext.declarative import declared_attr

from backend.app.db.base import Base


class BaseModel(Base):
    """Base model with common fields."""

    __abstract__ = True

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate __tablename__ automatically from class name."""
        return cls.__name__.lower()

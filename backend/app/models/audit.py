"""Audit Log model."""
from sqlalchemy import Column, String, DateTime, ForeignKey
from backend.app.models.base import BaseModel


class AuditLog(BaseModel):
    """Audit Log model."""
    __tablename__ = "audit_logs"

    company_id = Column(String, ForeignKey("companies.id"), index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False, index=True)
    entity_id = Column(String, index=True)
    old_values = Column(String)  # JSON
    new_values = Column(String)  # JSON
    ip_address = Column(String)
    user_agent = Column(String)
    timestamp = Column(DateTime, index=True)

"""Document model."""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from backend.app.models.base import BaseModel


class Document(BaseModel):
    """Document model for attachments."""
    __tablename__ = "documents"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    document_number = Column(String, nullable=False, index=True)
    document_type = Column(String, nullable=False)
    entity_type = Column(String)
    entity_id = Column(String, index=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String)
    file_hash = Column(String)
    description = Column(String)
    upload_date = Column(DateTime)
    uploaded_by = Column(String)
    is_processed = Column(Boolean, default=False, nullable=False)
    processing_status = Column(String)
    extraction_data = Column(String)  # JSON

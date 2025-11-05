"""Payment Terms model."""
from sqlalchemy import Column, String, Integer, Numeric, Boolean, ForeignKey
from backend.app.models.base import BaseModel


class PaymentTerms(BaseModel):
    """Payment Terms model."""
    __tablename__ = "payment_terms"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    net_days = Column(Integer, default=0, nullable=False)
    discount_percentage = Column(Numeric(5, 2), default=0)
    discount_days = Column(Integer, default=0)
    description = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)

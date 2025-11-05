"""Tax Code model."""
from sqlalchemy import Column, String, Numeric, Boolean, ForeignKey
from backend.app.models.base import BaseModel


class TaxCode(BaseModel):
    """Tax Code model."""
    __tablename__ = "tax_codes"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    tax_type = Column(String, nullable=False)
    rate = Column(Numeric(5, 2), nullable=False)
    description = Column(String)
    is_compound = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    tax_account_id = Column(String, ForeignKey("chart_of_accounts.id"))

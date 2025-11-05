"""Currency and Exchange Rate models."""
from sqlalchemy import Column, String, Integer, Boolean, Numeric, Date, ForeignKey
from backend.app.models.base import BaseModel


class Currency(BaseModel):
    """Currency model."""
    __tablename__ = "currencies"

    code = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    symbol = Column(String)
    decimal_places = Column(Integer, default=2)
    is_active = Column(Boolean, default=True, nullable=False)


class ExchangeRate(BaseModel):
    """Exchange Rate model."""
    __tablename__ = "exchange_rates"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    from_currency = Column(String, ForeignKey("currencies.code"), nullable=False)
    to_currency = Column(String, ForeignKey("currencies.code"), nullable=False)
    rate = Column(Numeric(10, 6), nullable=False)
    effective_date = Column(Date, nullable=False, index=True)
    source = Column(String)

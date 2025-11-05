"""Company, Fiscal Year, and Accounting Period models."""
from sqlalchemy import Column, String, Boolean, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.models.base import BaseModel


class Company(BaseModel):
    """Company model."""

    __tablename__ = "companies"

    code = Column(String, nullable=False, unique=True, index=True)
    name_en = Column(String, nullable=False)
    name_ar = Column(String)
    legal_name = Column(String)
    tax_id = Column(String)
    commercial_registration = Column(String)
    base_currency = Column(String, default="USD", nullable=False)
    fiscal_year_start = Column(Integer, default=1, nullable=False)  # Month 1-12
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    website = Column(String)
    logo_url = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    fiscal_years = relationship("FiscalYear", back_populates="company", cascade="all, delete-orphan")
    chart_of_accounts = relationship("ChartOfAccounts", back_populates="company")

    def __repr__(self):
        return f"<Company {self.code}>"


class FiscalYear(BaseModel):
    """Fiscal Year model."""

    __tablename__ = "fiscal_years"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    year_code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_closed = Column(Boolean, default=False, nullable=False)
    closed_at = Column(DateTime)
    closed_by = Column(String)

    # Relationships
    company = relationship("Company", back_populates="fiscal_years")
    periods = relationship("AccountingPeriod", back_populates="fiscal_year", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<FiscalYear {self.year_code}>"


class AccountingPeriod(BaseModel):
    """Accounting Period model."""

    __tablename__ = "accounting_periods"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    fiscal_year_id = Column(String, ForeignKey("fiscal_years.id"), nullable=False)
    period_number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_closed = Column(Boolean, default=False, nullable=False)
    closed_at = Column(DateTime)
    closed_by = Column(String)

    # Relationships
    fiscal_year = relationship("FiscalYear", back_populates="periods")

    def __repr__(self):
        return f"<AccountingPeriod {self.name}>"

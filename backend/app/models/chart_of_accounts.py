"""Chart of Accounts model."""
from sqlalchemy import Column, String, Boolean, Integer, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.models.base import BaseModel


class ChartOfAccounts(BaseModel):
    """Chart of Accounts model."""

    __tablename__ = "chart_of_accounts"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    account_code = Column(String, nullable=False, index=True)
    account_name_en = Column(String, nullable=False)
    account_name_ar = Column(String)
    parent_id = Column(String, ForeignKey("chart_of_accounts.id"))
    account_type = Column(String, nullable=False)  # ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE
    account_subtype = Column(String)  # CURRENT, NON_CURRENT, OPERATING, etc.
    account_nature = Column(String, nullable=False)  # DEBIT, CREDIT
    level = Column(Integer, nullable=False)
    is_parent = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    currency = Column(String)
    allow_manual_entry = Column(Boolean, default=True, nullable=False)
    description = Column(String)
    opening_balance = Column(Numeric(20, 4), default=0)
    opening_balance_date = Column(Date)

    # Relationships
    company = relationship("Company", back_populates="chart_of_accounts")
    parent = relationship("ChartOfAccounts", remote_side=[BaseModel.id], backref="children")

    def __repr__(self):
        return f"<Account {self.account_code} - {self.account_name_en}>"

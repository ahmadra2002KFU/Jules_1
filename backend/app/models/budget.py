"""Budget models."""
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.models.base import BaseModel


class Budget(BaseModel):
    """Budget model."""
    __tablename__ = "budgets"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    budget_code = Column(String, nullable=False, index=True)
    budget_name = Column(String, nullable=False)
    fiscal_year_id = Column(String, ForeignKey("fiscal_years.id"), nullable=False)
    budget_type = Column(String, default="ANNUAL")
    version = Column(String, default="ORIGINAL")
    status = Column(String, default="DRAFT")
    description = Column(String)
    approved_at = Column(DateTime)
    approved_by = Column(String)

    lines = relationship("BudgetLine", back_populates="budget", cascade="all, delete-orphan")


class BudgetLine(BaseModel):
    """Budget Line model."""
    __tablename__ = "budget_lines"

    budget_id = Column(String, ForeignKey("budgets.id"), nullable=False, index=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    account_id = Column(String, ForeignKey("chart_of_accounts.id"), nullable=False)
    cost_center_id = Column(String, ForeignKey("cost_centers.id"))
    project_id = Column(String, ForeignKey("projects.id"))
    period_id = Column(String, ForeignKey("accounting_periods.id"))
    budget_amount = Column(Numeric(20, 4), default=0, nullable=False)
    notes = Column(String)

    budget = relationship("Budget", back_populates="lines")

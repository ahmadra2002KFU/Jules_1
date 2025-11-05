"""Journal Entry and General Ledger models."""
from sqlalchemy import Column, String, Date, Numeric, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.models.base import BaseModel


class JournalEntry(BaseModel):
    """Journal Entry model."""

    __tablename__ = "journal_entries"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    entry_number = Column(String, nullable=False, index=True)
    entry_date = Column(Date, nullable=False, index=True)
    posting_date = Column(Date, nullable=False)
    fiscal_year_id = Column(String, ForeignKey("fiscal_years.id"), nullable=False)
    period_id = Column(String, ForeignKey("accounting_periods.id"), nullable=False)
    entry_type = Column(String, default="MANUAL", nullable=False)
    reference = Column(String)
    description = Column(String, nullable=False)
    status = Column(String, default="DRAFT", nullable=False, index=True)
    total_debit = Column(Numeric(20, 4), default=0, nullable=False)
    total_credit = Column(Numeric(20, 4), default=0, nullable=False)
    currency = Column(String, default="USD", nullable=False)
    exchange_rate = Column(Numeric(10, 6), default=1)
    is_reversed = Column(Boolean, default=False, nullable=False)
    reversed_entry_id = Column(String, ForeignKey("journal_entries.id"))
    reversal_date = Column(Date)
    source_document_type = Column(String)
    source_document_id = Column(String)
    approved_at = Column(DateTime)
    approved_by = Column(String)
    posted_at = Column(DateTime)
    posted_by = Column(String)

    # Relationships
    lines = relationship("JournalEntryLine", back_populates="journal_entry", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<JournalEntry {self.entry_number}>"


class JournalEntryLine(BaseModel):
    """Journal Entry Line model."""

    __tablename__ = "journal_entry_lines"

    journal_entry_id = Column(String, ForeignKey("journal_entries.id"), nullable=False, index=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    line_number = Column(Integer, nullable=False)
    account_id = Column(String, ForeignKey("chart_of_accounts.id"), nullable=False, index=True)
    debit_amount = Column(Numeric(20, 4), default=0, nullable=False)
    credit_amount = Column(Numeric(20, 4), default=0, nullable=False)
    description = Column(String)
    cost_center_id = Column(String, ForeignKey("cost_centers.id"))
    project_id = Column(String, ForeignKey("projects.id"))
    department_id = Column(String)
    currency = Column(String)
    exchange_rate = Column(Numeric(10, 6), default=1)
    reference = Column(String)

    # Relationships
    journal_entry = relationship("JournalEntry", back_populates="lines")

    def __repr__(self):
        return f"<JournalEntryLine {self.line_number}>"


class GeneralLedger(BaseModel):
    """General Ledger model."""

    __tablename__ = "general_ledger"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    account_id = Column(String, ForeignKey("chart_of_accounts.id"), nullable=False, index=True)
    entry_date = Column(Date, nullable=False, index=True)
    posting_date = Column(Date, nullable=False)
    fiscal_year_id = Column(String, ForeignKey("fiscal_years.id"), nullable=False)
    period_id = Column(String, ForeignKey("accounting_periods.id"), nullable=False, index=True)
    journal_entry_id = Column(String, ForeignKey("journal_entries.id"), nullable=False)
    journal_entry_line_id = Column(String, ForeignKey("journal_entry_lines.id"), nullable=False)
    debit_amount = Column(Numeric(20, 4), default=0, nullable=False)
    credit_amount = Column(Numeric(20, 4), default=0, nullable=False)
    running_balance = Column(Numeric(20, 4))
    description = Column(String)
    cost_center_id = Column(String, ForeignKey("cost_centers.id"))
    project_id = Column(String, ForeignKey("projects.id"))

    def __repr__(self):
        return f"<GeneralLedger {self.id}>"

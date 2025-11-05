"""Bank Account and Transaction models."""
from sqlalchemy import Column, String, Date, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.models.base import BaseModel


class BankAccount(BaseModel):
    """Bank Account model."""
    __tablename__ = "bank_accounts"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    account_code = Column(String, nullable=False, index=True)
    account_name = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    account_number = Column(String)
    iban = Column(String)
    swift_code = Column(String)
    branch_name = Column(String)
    currency = Column(String, default="USD", nullable=False)
    account_type = Column(String, default="CHECKING")
    gl_account_id = Column(String, ForeignKey("chart_of_accounts.id"), nullable=False)
    opening_balance = Column(Numeric(20, 4), default=0)
    current_balance = Column(Numeric(20, 4), default=0)
    is_active = Column(Boolean, default=True, nullable=False)


class BankTransaction(BaseModel):
    """Bank Transaction model."""
    __tablename__ = "bank_transactions"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    bank_account_id = Column(String, ForeignKey("bank_accounts.id"), nullable=False, index=True)
    transaction_date = Column(Date, nullable=False, index=True)
    value_date = Column(Date)
    description = Column(String)
    reference = Column(String)
    transaction_type = Column(String, nullable=False)
    amount = Column(Numeric(20, 4), nullable=False)
    balance = Column(Numeric(20, 4))
    is_reconciled = Column(Boolean, default=False, nullable=False)
    reconciliation_id = Column(String, ForeignKey("bank_reconciliations.id"))
    matched_journal_entry_id = Column(String, ForeignKey("journal_entries.id"))
    notes = Column(String)


class BankReconciliation(BaseModel):
    """Bank Reconciliation model."""
    __tablename__ = "bank_reconciliations"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    bank_account_id = Column(String, ForeignKey("bank_accounts.id"), nullable=False, index=True)
    reconciliation_date = Column(Date, nullable=False)
    statement_date = Column(Date, nullable=False)
    statement_balance = Column(Numeric(20, 4), nullable=False)
    gl_balance = Column(Numeric(20, 4), nullable=False)
    adjusted_balance = Column(Numeric(20, 4))
    is_balanced = Column(Boolean, default=False, nullable=False)
    status = Column(String, default="IN_PROGRESS", nullable=False)
    notes = Column(String)

"""Payment model."""
from sqlalchemy import Column, String, Date, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.models.base import BaseModel


class Payment(BaseModel):
    """Payment model."""

    __tablename__ = "payments"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    payment_number = Column(String, nullable=False, index=True)
    payment_type = Column(String, nullable=False, index=True)  # RECEIPT (AR), PAYMENT (AP)
    payment_date = Column(Date, nullable=False, index=True)
    fiscal_year_id = Column(String, ForeignKey("fiscal_years.id"), nullable=False)
    period_id = Column(String, ForeignKey("accounting_periods.id"), nullable=False)
    party_type = Column(String, nullable=False)  # CUSTOMER, VENDOR
    party_id = Column(String, nullable=False, index=True)  # customer_id or vendor_id
    payment_method = Column(String, nullable=False)  # CASH, CHECK, BANK_TRANSFER, CREDIT_CARD
    bank_account_id = Column(String, ForeignKey("bank_accounts.id"))
    reference = Column(String)
    check_number = Column(String)
    check_date = Column(Date)
    currency = Column(String, default="USD", nullable=False)
    exchange_rate = Column(Numeric(10, 6), default=1)
    total_amount = Column(Numeric(20, 4), default=0, nullable=False)
    allocated_amount = Column(Numeric(20, 4), default=0)
    unallocated_amount = Column(Numeric(20, 4), default=0)
    status = Column(String, default="DRAFT", nullable=False, index=True)
    notes = Column(String)
    journal_entry_id = Column(String, ForeignKey("journal_entries.id"))
    is_posted = Column(Boolean, default=False, nullable=False)
    posted_at = Column(DateTime)
    posted_by = Column(String)

    # Relationships
    allocations = relationship("PaymentAllocation", back_populates="payment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Payment {self.payment_number}>"


class PaymentAllocation(BaseModel):
    """Payment Allocation model."""

    __tablename__ = "payment_allocations"

    payment_id = Column(String, ForeignKey("payments.id"), nullable=False, index=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    document_type = Column(String, nullable=False)  # INVOICE, BILL
    document_id = Column(String, nullable=False, index=True)  # invoice_id or bill_id
    allocated_amount = Column(Numeric(20, 4), default=0, nullable=False)
    allocation_date = Column(Date, nullable=False)
    notes = Column(String)

    # Relationships
    payment = relationship("Payment", back_populates="allocations")

    def __repr__(self):
        return f"<PaymentAllocation {self.id}>"

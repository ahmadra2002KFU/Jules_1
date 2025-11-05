"""Bill model."""
from sqlalchemy import Column, String, Date, Numeric, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.models.base import BaseModel


class Bill(BaseModel):
    """Bill model."""

    __tablename__ = "bills"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    bill_number = Column(String, nullable=False, index=True)
    bill_type = Column(String, default="STANDARD", nullable=False)
    bill_date = Column(Date, nullable=False, index=True)
    due_date = Column(Date, nullable=False)
    vendor_id = Column(String, ForeignKey("vendors.id"), nullable=False, index=True)
    vendor_invoice_number = Column(String)
    fiscal_year_id = Column(String, ForeignKey("fiscal_years.id"), nullable=False)
    period_id = Column(String, ForeignKey("accounting_periods.id"), nullable=False)
    currency = Column(String, default="USD", nullable=False)
    exchange_rate = Column(Numeric(10, 6), default=1)
    subtotal = Column(Numeric(20, 4), default=0, nullable=False)
    discount_percentage = Column(Numeric(5, 2), default=0)
    discount_amount = Column(Numeric(20, 4), default=0)
    tax_amount = Column(Numeric(20, 4), default=0)
    total_amount = Column(Numeric(20, 4), default=0, nullable=False)
    paid_amount = Column(Numeric(20, 4), default=0)
    balance_amount = Column(Numeric(20, 4), default=0, nullable=False)
    status = Column(String, default="DRAFT", nullable=False, index=True)
    payment_terms_id = Column(String, ForeignKey("payment_terms.id"))
    reference = Column(String)
    notes = Column(String)
    internal_notes = Column(String)
    journal_entry_id = Column(String, ForeignKey("journal_entries.id"))
    related_bill_id = Column(String, ForeignKey("bills.id"))
    purchase_order_id = Column(String)
    is_posted = Column(Boolean, default=False, nullable=False)
    posted_at = Column(DateTime)
    posted_by = Column(String)
    approved_at = Column(DateTime)
    approved_by = Column(String)

    # Relationships
    vendor = relationship("Vendor", back_populates="bills")
    lines = relationship("BillLine", back_populates="bill", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Bill {self.bill_number}>"


class BillLine(BaseModel):
    """Bill Line model."""

    __tablename__ = "bill_lines"

    bill_id = Column(String, ForeignKey("bills.id"), nullable=False, index=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    line_number = Column(Integer, nullable=False)
    item_id = Column(String, ForeignKey("items.id"))
    description = Column(String, nullable=False)
    quantity = Column(Numeric(20, 4), default=1, nullable=False)
    unit_price = Column(Numeric(20, 4), default=0, nullable=False)
    discount_percentage = Column(Numeric(5, 2), default=0)
    discount_amount = Column(Numeric(20, 4), default=0)
    tax_code_id = Column(String, ForeignKey("tax_codes.id"))
    tax_percentage = Column(Numeric(5, 2), default=0)
    tax_amount = Column(Numeric(20, 4), default=0)
    line_total = Column(Numeric(20, 4), default=0, nullable=False)
    account_id = Column(String, ForeignKey("chart_of_accounts.id"))
    cost_center_id = Column(String, ForeignKey("cost_centers.id"))
    project_id = Column(String, ForeignKey("projects.id"))

    # Relationships
    bill = relationship("Bill", back_populates="lines")

    def __repr__(self):
        return f"<BillLine {self.line_number}>"

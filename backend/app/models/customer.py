"""Customer model."""
from sqlalchemy import Column, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.models.base import BaseModel


class Customer(BaseModel):
    """Customer model."""

    __tablename__ = "customers"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    customer_code = Column(String, nullable=False, index=True)
    customer_name_en = Column(String, nullable=False, index=True)
    customer_name_ar = Column(String)
    customer_type = Column(String, default="REGULAR")
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    mobile = Column(String)
    website = Column(String)
    tax_id = Column(String)
    commercial_registration = Column(String)
    billing_address = Column(String)
    shipping_address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)
    payment_terms_id = Column(String, ForeignKey("payment_terms.id"))
    credit_limit = Column(Numeric(20, 4), default=0)
    price_list_id = Column(String)
    salesperson_id = Column(String)
    account_id = Column(String, ForeignKey("chart_of_accounts.id"))
    is_active = Column(Boolean, default=True, nullable=False)
    notes = Column(String)

    # Relationships
    invoices = relationship("Invoice", back_populates="customer")

    def __repr__(self):
        return f"<Customer {self.customer_code}>"

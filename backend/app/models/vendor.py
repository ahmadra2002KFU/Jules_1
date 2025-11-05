"""Vendor model."""
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.models.base import BaseModel


class Vendor(BaseModel):
    """Vendor model."""

    __tablename__ = "vendors"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    vendor_code = Column(String, nullable=False, index=True)
    vendor_name_en = Column(String, nullable=False, index=True)
    vendor_name_ar = Column(String)
    vendor_type = Column(String, default="REGULAR")
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    mobile = Column(String)
    website = Column(String)
    tax_id = Column(String)
    commercial_registration = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)
    payment_terms_id = Column(String, ForeignKey("payment_terms.id"))
    bank_name = Column(String)
    bank_account_number = Column(String)
    iban = Column(String)
    swift_code = Column(String)
    payment_method = Column(String)
    account_id = Column(String, ForeignKey("chart_of_accounts.id"))
    is_active = Column(Boolean, default=True, nullable=False)
    notes = Column(String)

    # Relationships
    bills = relationship("Bill", back_populates="vendor")

    def __repr__(self):
        return f"<Vendor {self.vendor_code}>"

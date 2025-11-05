"""Fixed Asset models."""
from sqlalchemy import Column, String, Numeric, Boolean, Date, Integer, ForeignKey
from backend.app.models.base import BaseModel


class AssetCategory(BaseModel):
    """Asset Category model."""
    __tablename__ = "asset_categories"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    depreciation_method = Column(String, default="STRAIGHT_LINE")
    useful_life_years = Column(Integer)
    salvage_value_percentage = Column(Numeric(5, 2))
    asset_account_id = Column(String, ForeignKey("chart_of_accounts.id"))
    depreciation_account_id = Column(String, ForeignKey("chart_of_accounts.id"))
    accumulated_depreciation_account_id = Column(String, ForeignKey("chart_of_accounts.id"))
    is_active = Column(Boolean, default=True, nullable=False)


class FixedAsset(BaseModel):
    """Fixed Asset model."""
    __tablename__ = "fixed_assets"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    asset_code = Column(String, nullable=False, index=True)
    asset_name = Column(String, nullable=False)
    category_id = Column(String, ForeignKey("asset_categories.id"), nullable=False)
    serial_number = Column(String)
    description = Column(String)
    purchase_date = Column(Date, nullable=False)
    purchase_cost = Column(Numeric(20, 4), nullable=False)
    salvage_value = Column(Numeric(20, 4), default=0)
    useful_life_years = Column(Integer, nullable=False)
    depreciation_method = Column(String, nullable=False)
    depreciation_start_date = Column(Date)
    location = Column(String)
    custodian = Column(String)
    vendor_id = Column(String, ForeignKey("vendors.id"))
    warranty_expiry_date = Column(Date)
    status = Column(String, default="ACTIVE")
    disposal_date = Column(Date)
    disposal_amount = Column(Numeric(20, 4))
    disposal_notes = Column(String)
    image_url = Column(String)


class DepreciationSchedule(BaseModel):
    """Depreciation Schedule model."""
    __tablename__ = "depreciation_schedules"

    asset_id = Column(String, ForeignKey("fixed_assets.id"), nullable=False, index=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    fiscal_year_id = Column(String, ForeignKey("fiscal_years.id"), nullable=False)
    period_id = Column(String, ForeignKey("accounting_periods.id"), nullable=False)
    depreciation_date = Column(Date, nullable=False)
    opening_book_value = Column(Numeric(20, 4), nullable=False)
    depreciation_amount = Column(Numeric(20, 4), nullable=False)
    accumulated_depreciation = Column(Numeric(20, 4), nullable=False)
    closing_book_value = Column(Numeric(20, 4), nullable=False)
    journal_entry_id = Column(String, ForeignKey("journal_entries.id"))
    is_posted = Column(Boolean, default=False, nullable=False)

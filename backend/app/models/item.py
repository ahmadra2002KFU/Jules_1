"""Inventory Item models."""
from sqlalchemy import Column, String, Numeric, Boolean, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship
from backend.app.models.base import BaseModel


class ItemCategory(BaseModel):
    """Item Category model."""
    __tablename__ = "item_categories"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    name_en = Column(String, nullable=False)
    name_ar = Column(String)
    parent_id = Column(String, ForeignKey("item_categories.id"))
    description = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)


class Item(BaseModel):
    """Inventory Item model."""
    __tablename__ = "items"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    item_code = Column(String, nullable=False, index=True)
    item_name_en = Column(String, nullable=False, index=True)
    item_name_ar = Column(String)
    category_id = Column(String, ForeignKey("item_categories.id"))
    item_type = Column(String, default="INVENTORY", nullable=False)
    unit_of_measure = Column(String, nullable=False)
    barcode = Column(String, index=True)
    sku = Column(String)
    description = Column(String)
    costing_method = Column(String, default="WEIGHTED_AVG", nullable=False)
    standard_cost = Column(Numeric(20, 4), default=0)
    sales_price = Column(Numeric(20, 4), default=0)
    purchase_price = Column(Numeric(20, 4), default=0)
    reorder_level = Column(Numeric(20, 4), default=0)
    reorder_quantity = Column(Numeric(20, 4), default=0)
    track_inventory = Column(Boolean, default=True, nullable=False)
    track_serial_numbers = Column(Boolean, default=False, nullable=False)
    track_lot_numbers = Column(Boolean, default=False, nullable=False)
    sales_account_id = Column(String, ForeignKey("chart_of_accounts.id"))
    purchase_account_id = Column(String, ForeignKey("chart_of_accounts.id"))
    inventory_account_id = Column(String, ForeignKey("chart_of_accounts.id"))
    cogs_account_id = Column(String, ForeignKey("chart_of_accounts.id"))
    default_tax_code_id = Column(String, ForeignKey("tax_codes.id"))
    image_url = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)


class Warehouse(BaseModel):
    """Warehouse model."""
    __tablename__ = "warehouses"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)


class InventoryTransaction(BaseModel):
    """Inventory Transaction model."""
    __tablename__ = "inventory_transactions"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    transaction_number = Column(String, nullable=False, index=True)
    transaction_date = Column(Date, nullable=False, index=True)
    transaction_type = Column(String, nullable=False)
    item_id = Column(String, ForeignKey("items.id"), nullable=False, index=True)
    warehouse_id = Column(String, ForeignKey("warehouses.id"), nullable=False, index=True)
    quantity = Column(Numeric(20, 4), nullable=False)
    unit_cost = Column(Numeric(20, 4))
    total_cost = Column(Numeric(20, 4))
    reference = Column(String)
    notes = Column(String)
    source_document_type = Column(String)
    source_document_id = Column(String)
    journal_entry_id = Column(String, ForeignKey("journal_entries.id"))


class StockLevel(BaseModel):
    """Stock Level model."""
    __tablename__ = "stock_levels"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    item_id = Column(String, ForeignKey("items.id"), nullable=False, index=True)
    warehouse_id = Column(String, ForeignKey("warehouses.id"), nullable=False, index=True)
    quantity_on_hand = Column(Numeric(20, 4), default=0)
    quantity_committed = Column(Numeric(20, 4), default=0)
    quantity_available = Column(Numeric(20, 4), default=0)
    quantity_on_order = Column(Numeric(20, 4), default=0)
    average_cost = Column(Numeric(20, 4), default=0)
    total_value = Column(Numeric(20, 4), default=0)

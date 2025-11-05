"""Cost Center and Project models."""
from sqlalchemy import Column, String, Boolean, Numeric, Date, ForeignKey
from backend.app.models.base import BaseModel


class CostCenter(BaseModel):
    """Cost Center model."""
    __tablename__ = "cost_centers"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    name_en = Column(String, nullable=False)
    name_ar = Column(String)
    parent_id = Column(String, ForeignKey("cost_centers.id"))
    type = Column(String, default="DEPARTMENT")
    manager = Column(String)
    description = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)


class Project(BaseModel):
    """Project model."""
    __tablename__ = "projects"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    customer_id = Column(String, ForeignKey("customers.id"))
    project_manager = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Numeric(20, 4))
    status = Column(String, default="ACTIVE")
    is_billable = Column(Boolean, default=True, nullable=False)

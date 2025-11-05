"""Company endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.app.db.base import get_db

router = APIRouter()

@router.get("/")
async def get_companies(db: AsyncSession = Depends(get_db)):
    """Get all companies."""
    return {"companies": [], "total": 0}

@router.post("/")
async def create_company(db: AsyncSession = Depends(get_db)):
    """Create a new company."""
    return {"message": "Company created successfully"}

@router.get("/{company_id}")
async def get_company(company_id: str, db: AsyncSession = Depends(get_db)):
    """Get company by ID."""
    return {"id": company_id, "name": "Sample Company"}

@router.put("/{company_id}")
async def update_company(company_id: str, db: AsyncSession = Depends(get_db)):
    """Update company."""
    return {"message": "Company updated successfully"}

@router.delete("/{company_id}")
async def delete_company(company_id: str, db: AsyncSession = Depends(get_db)):
    """Delete company."""
    return {"message": "Company deleted successfully"}

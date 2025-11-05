"""Vendors endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.base import get_db

router = APIRouter()

@router.get("/")
async def get_vendors(company_id: str, db: AsyncSession = Depends(get_db)):
    """Get all vendors."""
    return {"items": [], "total": 0}

@router.post("/")
async def create_item(db: AsyncSession = Depends(get_db)):
    """Create a new item."""
    return {"message": "Item created successfully"}

@router.get("/{item_id}")
async def get_item(item_id: str, db: AsyncSession = Depends(get_db)):
    """Get item by ID."""
    return {"id": item_id}

@router.put("/{item_id}")
async def update_item(item_id: str, db: AsyncSession = Depends(get_db)):
    """Update item."""
    return {"message": "Item updated successfully"}

@router.delete("/{item_id}")
async def delete_item(item_id: str, db: AsyncSession = Depends(get_db)):
    """Delete item."""
    return {"message": "Item deleted successfully"}

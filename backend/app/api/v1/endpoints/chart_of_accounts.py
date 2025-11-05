"""Chart of Accounts endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.base import get_db

router = APIRouter()

@router.get("/")
async def get_chart_of_accounts(company_id: str, db: AsyncSession = Depends(get_db)):
    """Get chart of accounts for a company."""
    return {"accounts": [], "total": 0}

@router.post("/")
async def create_account(db: AsyncSession = Depends(get_db)):
    """Create a new account."""
    return {"message": "Account created successfully"}

@router.get("/{account_id}")
async def get_account(account_id: str, db: AsyncSession = Depends(get_db)):
    """Get account by ID."""
    return {"id": account_id}

@router.put("/{account_id}")
async def update_account(account_id: str, db: AsyncSession = Depends(get_db)):
    """Update account."""
    return {"message": "Account updated successfully"}

@router.delete("/{account_id}")
async def delete_account(account_id: str, db: AsyncSession = Depends(get_db)):
    """Delete account."""
    return {"message": "Account deleted successfully"}

@router.get("/tree")
async def get_account_tree(company_id: str, db: AsyncSession = Depends(get_db)):
    """Get hierarchical account tree."""
    return {"tree": []}

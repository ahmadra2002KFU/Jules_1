"""Journal Entry endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.base import get_db

router = APIRouter()

@router.get("/")
async def get_journal_entries(company_id: str, db: AsyncSession = Depends(get_db)):
    """Get all journal entries."""
    return {"entries": [], "total": 0}

@router.post("/")
async def create_journal_entry(db: AsyncSession = Depends(get_db)):
    """Create a new journal entry."""
    return {"message": "Journal entry created successfully"}

@router.get("/{entry_id}")
async def get_journal_entry(entry_id: str, db: AsyncSession = Depends(get_db)):
    """Get journal entry by ID."""
    return {"id": entry_id}

@router.put("/{entry_id}")
async def update_journal_entry(entry_id: str, db: AsyncSession = Depends(get_db)):
    """Update journal entry."""
    return {"message": "Journal entry updated successfully"}

@router.post("/{entry_id}/post")
async def post_journal_entry(entry_id: str, db: AsyncSession = Depends(get_db)):
    """Post journal entry to general ledger."""
    return {"message": "Journal entry posted successfully"}

@router.post("/{entry_id}/reverse")
async def reverse_journal_entry(entry_id: str, db: AsyncSession = Depends(get_db)):
    """Reverse a posted journal entry."""
    return {"message": "Journal entry reversed successfully"}

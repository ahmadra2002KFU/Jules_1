"""Dashboard endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.base import get_db

router = APIRouter()

@router.get("/")
async def get_dashboard(company_id: str, db: AsyncSession = Depends(get_db)):
    """Get dashboard data."""
    return {
        "kpis": {
            "revenue": {"current": 0, "previous": 0, "change_percent": 0},
            "expenses": {"current": 0, "previous": 0, "change_percent": 0},
            "profit": {"current": 0, "previous": 0, "change_percent": 0},
            "cash": {"current": 0, "previous": 0, "change_percent": 0},
        },
        "charts": {
            "revenue_trend": [],
            "expense_breakdown": [],
            "ar_aging": [],
            "ap_aging": [],
        },
        "recent_transactions": [],
        "alerts": [],
    }

@router.get("/kpis")
async def get_kpis(company_id: str, db: AsyncSession = Depends(get_db)):
    """Get key performance indicators."""
    return {"kpis": {}}

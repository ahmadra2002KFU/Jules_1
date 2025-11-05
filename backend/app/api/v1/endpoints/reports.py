"""Reporting endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.base import get_db

router = APIRouter()

@router.get("/balance-sheet")
async def get_balance_sheet(company_id: str, as_of_date: str, db: AsyncSession = Depends(get_db)):
    """Generate Balance Sheet."""
    return {
        "report_name": "Balance Sheet",
        "as_of_date": as_of_date,
        "assets": {"total": 0, "items": []},
        "liabilities": {"total": 0, "items": []},
        "equity": {"total": 0, "items": []},
    }

@router.get("/income-statement")
async def get_income_statement(
    company_id: str, start_date: str, end_date: str, db: AsyncSession = Depends(get_db)
):
    """Generate Income Statement."""
    return {
        "report_name": "Income Statement",
        "period": f"{start_date} to {end_date}",
        "revenue": {"total": 0, "items": []},
        "expenses": {"total": 0, "items": []},
        "net_income": 0,
    }

@router.get("/cash-flow")
async def get_cash_flow(
    company_id: str, start_date: str, end_date: str, db: AsyncSession = Depends(get_db)
):
    """Generate Cash Flow Statement."""
    return {
        "report_name": "Cash Flow Statement",
        "period": f"{start_date} to {end_date}",
        "operating_activities": 0,
        "investing_activities": 0,
        "financing_activities": 0,
        "net_change": 0,
    }

@router.get("/trial-balance")
async def get_trial_balance(company_id: str, as_of_date: str, db: AsyncSession = Depends(get_db)):
    """Generate Trial Balance."""
    return {
        "report_name": "Trial Balance",
        "as_of_date": as_of_date,
        "accounts": [],
        "total_debit": 0,
        "total_credit": 0,
    }

@router.get("/general-ledger")
async def get_general_ledger(
    company_id: str, account_id: str, start_date: str, end_date: str,
    db: AsyncSession = Depends(get_db)
):
    """Generate General Ledger report."""
    return {
        "report_name": "General Ledger",
        "account": {},
        "transactions": [],
    }

@router.get("/ar-aging")
async def get_ar_aging(company_id: str, as_of_date: str, db: AsyncSession = Depends(get_db)):
    """Generate AR Aging Report."""
    return {
        "report_name": "AR Aging",
        "as_of_date": as_of_date,
        "customers": [],
        "total": 0,
    }

@router.get("/ap-aging")
async def get_ap_aging(company_id: str, as_of_date: str, db: AsyncSession = Depends(get_db)):
    """Generate AP Aging Report."""
    return {
        "report_name": "AP Aging",
        "as_of_date": as_of_date,
        "vendors": [],
        "total": 0,
    }

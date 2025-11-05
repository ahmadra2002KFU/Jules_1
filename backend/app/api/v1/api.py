"""
Main API router that includes all endpoint routers.
"""
from fastapi import APIRouter

from backend.app.api.v1.endpoints import (
    auth,
    companies,
    chart_of_accounts,
    journal_entries,
    invoices,
    bills,
    payments,
    customers,
    vendors,
    bank_accounts,
    items,
    reports,
    ai_assistant,
    dashboard,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(chart_of_accounts.router, prefix="/chart-of-accounts", tags=["Chart of Accounts"])
api_router.include_router(journal_entries.router, prefix="/journal-entries", tags=["Journal Entries"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
api_router.include_router(bills.router, prefix="/bills", tags=["Bills"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(customers.router, prefix="/customers", tags=["Customers"])
api_router.include_router(vendors.router, prefix="/vendors", tags=["Vendors"])
api_router.include_router(bank_accounts.router, prefix="/bank-accounts", tags=["Bank Accounts"])
api_router.include_router(items.router, prefix="/items", tags=["Inventory Items"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(ai_assistant.router, prefix="/ai", tags=["AI Assistant"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

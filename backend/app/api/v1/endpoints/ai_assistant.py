"""AI Assistant endpoints powered by Google Gemini."""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid

from backend.app.db.base import get_db
from backend.app.services.ai_service import ai_service

router = APIRouter()


# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    success: bool
    response: str
    suggestions: list = []
    actions: list = []
    session_id: str
    error: Optional[str] = None


class TransactionCategorizationRequest(BaseModel):
    description: str
    amount: float
    company_id: str


class InsightsRequest(BaseModel):
    company_id: str
    financial_data: Dict[str, Any]


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    company_id: str,
    user_id: str = "demo-user",  # TODO: Get from auth
    db: AsyncSession = Depends(get_db)
):
    """
    Chat with AI assistant powered by Google Gemini.

    Example queries:
    - "Show me unpaid invoices over 30 days"
    - "What's my current cash balance?"
    - "Generate P&L for Q3 2024"
    - "How do I record a loan?"
    """
    session_id = request.session_id or str(uuid.uuid4())

    result = await ai_service.chat(
        message=request.message,
        company_id=company_id,
        user_id=user_id,
        session_id=session_id,
        context=request.context or {},
        db=db
    )

    if result.get("success"):
        return ChatResponse(
            success=True,
            response=result["response"],
            suggestions=result.get("suggestions", []),
            actions=result.get("actions", []),
            session_id=session_id
        )
    else:
        return ChatResponse(
            success=False,
            response="I apologize, but I encountered an error. Please try again.",
            session_id=session_id,
            error=result.get("error")
        )


@router.post("/process-document")
async def process_document(
    file: UploadFile = File(...),
    company_id: str = "demo-company",  # TODO: Get from auth
    db: AsyncSession = Depends(get_db)
):
    """
    Process invoice/receipt using Gemini Vision OCR.

    Upload an image or PDF of an invoice/receipt and get structured data extracted.

    Returns:
    - document_type: Type of document (invoice, receipt, bill)
    - extracted_data: Structured data (vendor, date, amount, line items, etc.)
    - confidence: Confidence score (0-1)
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Read file content
    file_content = await file.read()

    if len(file_content) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    # Process with Gemini Vision
    result = await ai_service.process_document(
        file_content=file_content,
        file_type=file.content_type,
        company_id=company_id,
        db=db
    )

    if result.get("success"):
        return {
            "success": True,
            "document_type": result["document_type"],
            "extracted_data": result["extracted_data"],
            "confidence": result["confidence"],
            "message": f"Document processed successfully with {result['confidence']*100:.0f}% confidence"
        }
    else:
        return {
            "success": False,
            "error": result.get("error", "Failed to process document"),
            "message": "Could not extract data from document. Please try a clearer image."
        }


@router.post("/categorize-transaction")
async def categorize_transaction(
    request: TransactionCategorizationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Auto-categorize a transaction using Gemini AI.

    Analyzes the transaction description and amount to suggest the most appropriate
    account from the company's Chart of Accounts.

    Example:
    - "STARBUCKS COFFEE #1234" → Suggests "Office Meals & Entertainment"
    - "MONTHLY RENT PAYMENT" → Suggests "Rent Expense"
    """
    result = await ai_service.categorize_transaction(
        description=request.description,
        amount=request.amount,
        company_id=request.company_id,
        db=db
    )

    if result.get("success"):
        return {
            "success": True,
            "suggested_account": result["account_name"],
            "suggested_account_code": result["account_code"],
            "suggested_account_id": result["account_id"],
            "confidence": result["confidence"],
            "reasoning": result["reasoning"]
        }
    else:
        return {
            "success": False,
            "error": result.get("error"),
            "message": "Could not categorize transaction"
        }


@router.post("/insights")
async def get_insights(
    request: InsightsRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get AI-powered financial insights using Gemini.

    Analyzes financial data to provide:
    - Alerts about unusual patterns
    - Recommendations for improvement
    - Observations about trends
    - Opportunities to optimize

    Example financial_data:
    {
      "revenue_current_month": 50000,
      "revenue_last_month": 45000,
      "expenses_current_month": 38000,
      "expenses_last_month": 30000,
      "cash_balance": 15000,
      "ar_overdue": 12000,
      "ap_overdue": 8000
    }
    """
    result = await ai_service.generate_insights(
        company_id=request.company_id,
        financial_data=request.financial_data,
        db=db
    )

    if result.get("success"):
        return {
            "success": True,
            "insights": result["insights"],
            "generated_at": result["generated_at"],
            "count": len(result["insights"])
        }
    else:
        return {
            "success": False,
            "error": result.get("error"),
            "insights": []
        }


@router.post("/predict/cash-flow")
async def predict_cash_flow(
    company_id: str,
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    """
    Predict future cash flow using AI (Coming Soon).

    This endpoint will use historical cash flow data, outstanding AR/AP,
    and machine learning to forecast cash position.

    Args:
    - days: Number of days to forecast (30, 60, or 90)

    Returns:
    - Daily cash flow predictions
    - Confidence intervals
    - Key assumptions
    """
    # TODO: Implement with Prophet or ARIMA
    return {
        "success": False,
        "message": "Cash flow prediction feature coming soon",
        "note": "This will use time series forecasting with Prophet/ARIMA",
        "predictions": [],
        "confidence": 0.0,
        "model_version": "v1.0-pending"
    }


@router.post("/predict/sales")
async def predict_sales(
    company_id: str,
    days: int = 30,
    product_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Predict future sales using AI (Coming Soon).

    This endpoint will use historical sales data and seasonality patterns
    to forecast future sales.

    Args:
    - days: Number of days to forecast
    - product_id: Specific product (optional, for product-level forecast)

    Returns:
    - Sales predictions by day
    - Confidence intervals
    - Seasonal adjustments
    """
    # TODO: Implement with Prophet or LSTM
    return {
        "success": False,
        "message": "Sales prediction feature coming soon",
        "note": "This will use time series forecasting with seasonal decomposition",
        "predictions": [],
        "confidence": 0.0,
        "model_version": "v1.0-pending"
    }


@router.get("/health")
async def ai_health_check():
    """Check if AI service is available and configured."""
    return {
        "ai_enabled": ai_service.enabled,
        "provider": "Google Gemini",
        "models": {
            "text": "gemini-pro",
            "vision": "gemini-pro-vision"
        },
        "features": {
            "document_ocr": ai_service.enabled,
            "auto_categorization": ai_service.enabled,
            "chat_assistant": ai_service.enabled,
            "financial_insights": ai_service.enabled,
            "predictions": False  # Coming soon
        }
    }

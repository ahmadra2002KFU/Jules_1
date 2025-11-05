# AI Integration Guide - Where AI is Used in the App

## 📊 Current Status: **Infrastructure Ready, Implementation Needed**

The app has a complete **AI-ready infrastructure** with endpoints, models, and configuration in place. The actual AI service implementation needs to be completed.

---

## 🎯 AI Features & Their Locations

### 1. 🤖 **AI Chat Assistant**
**Location**: `/api/v1/ai/chat`
**File**: `backend/app/api/v1/endpoints/ai_assistant.py:8-16`

**What it does**:
- Natural language interface for accounting queries
- Examples: "Show unpaid invoices", "What's my cash balance?"

**Current Status**: ⚠️ Stub endpoint (returns mock response)

**Where it's used**:
- User asks questions about their financial data
- Generate reports via natural language
- Get explanations of accounting concepts
- Create transactions via voice/text

---

### 2. 📄 **Document OCR & Data Extraction**
**Location**: `/api/v1/ai/process-document`
**File**: `backend/app/api/v1/endpoints/ai_assistant.py:18-30`

**What it does**:
- Upload receipt/invoice image or PDF
- Extract vendor, date, amount, line items, tax
- Automatically create bill or expense entry

**Current Status**: ⚠️ Stub endpoint (returns mock data)

**Where it's used**:
- When user uploads a receipt → Creates expense entry
- When user uploads vendor invoice → Creates bill
- When user uploads bank statement → Imports transactions
- Mobile app: Take photo of receipt → Auto-processed

**Technologies Planned**:
- Tesseract OCR for text extraction
- OpenAI GPT-4 Vision for understanding document structure
- Pattern matching for data extraction

---

### 3. 🏷️ **Auto-Categorization**
**Location**: `/api/v1/ai/categorize-transaction`
**File**: `backend/app/api/v1/endpoints/ai_assistant.py:32-40`

**What it does**:
- Analyze transaction description
- Suggest appropriate account from Chart of Accounts
- Learn from user corrections

**Current Status**: ⚠️ Stub endpoint (returns mock suggestion)

**Where it's used**:
- When creating journal entries manually
- When importing bank transactions
- When processing credit card statements
- During bank reconciliation

**How it learns**:
- Stores training data in `ai_training_data` table
- User corrections improve suggestions
- Company-specific patterns

---

### 4. 💡 **Financial Insights**
**Location**: `/api/v1/ai/insights`
**File**: `backend/app/api/v1/endpoints/ai_assistant.py:42-60`

**What it does**:
- Analyze financial patterns
- Detect anomalies
- Provide recommendations
- Alert on unusual activity

**Current Status**: ⚠️ Stub endpoint (returns mock insights)

**Where it's used**:
- Dashboard: Display key insights
- Email alerts: Notify about unusual patterns
- Reports: Add AI commentary
- Decision support: Suggest actions

**Example Insights**:
- "Office expenses up 45% this month"
- "3 overdue invoices totaling $15,000"
- "Cash flow may be negative next month"
- "Consider negotiating better terms with Vendor X"

---

### 5. 📈 **Cash Flow Prediction**
**Location**: `/api/v1/ai/predict/cash-flow`
**File**: `backend/app/api/v1/endpoints/ai_assistant.py:62-69`

**What it does**:
- Forecast cash position for 30/60/90 days
- Based on historical data + outstanding AR/AP
- Confidence intervals (best/worst/expected)

**Current Status**: ⚠️ Stub endpoint (returns empty predictions)

**Where it's used**:
- Dashboard: Cash flow chart with projections
- Alerts: Warn about potential cash shortages
- Reports: Cash flow forecast report
- Planning: What-if scenarios

**Technologies Planned**:
- Prophet (Facebook's time series forecasting)
- Or ARIMA/LSTM models
- scikit-learn for ML

---

### 6. 📊 **Sales Forecasting**
**Location**: `/api/v1/ai/predict/sales`
**File**: `backend/app/api/v1/endpoints/ai_assistant.py:71-78`

**What it does**:
- Predict future sales trends
- Product-level or category-level forecasts
- Seasonal adjustments

**Current Status**: ⚠️ Stub endpoint (returns empty predictions)

**Where it's used**:
- Inventory planning
- Budget preparation
- Sales dashboards
- Business planning

---

## 🗄️ AI Database Tables

### 1. **ai_training_data**
**File**: `backend/app/models/ai.py:6-17`

**Purpose**: Store training data for machine learning

**Fields**:
- `company_id` - Multi-tenancy
- `data_type` - CATEGORIZATION, MATCHING, PREDICTION
- `input_data` - JSON with input features
- `output_data` - JSON with expected output
- `confidence_score` - Model confidence
- `is_validated` - User confirmed this is correct
- `validated_by` - Who validated it

**Example Use Case**:
```python
# When user corrects an auto-categorization
{
  "data_type": "CATEGORIZATION",
  "input_data": {
    "description": "STARBUCKS COFFEE #1234",
    "amount": 15.50
  },
  "output_data": {
    "account_id": "acc-office-meals",
    "account_code": "5230"
  },
  "is_validated": True,
  "confidence_score": 0.95
}
```

### 2. **ai_predictions**
**File**: `backend/app/models/ai.py:20-34`

**Purpose**: Store AI predictions and track accuracy

**Fields**:
- `prediction_type` - CASH_FLOW, SALES, EXPENSE
- `entity_type` - What was predicted
- `input_features` - Data used for prediction
- `prediction_value` - The prediction
- `confidence_score` - How confident
- `actual_value` - What actually happened (for learning)
- `accuracy_score` - How accurate was the prediction

**Example Use Case**:
```python
# Cash flow prediction
{
  "prediction_type": "CASH_FLOW",
  "input_features": {
    "historical_cash_flow": [...],
    "outstanding_ar": 50000,
    "outstanding_ap": 30000
  },
  "prediction_value": {
    "day_30": 25000,
    "day_60": 18000,
    "day_90": 22000
  },
  "confidence_score": 0.82,
  "model_version": "v1.0"
}
```

### 3. **ai_chat_history**
**File**: `backend/app/models/ai.py:37-47`

**Purpose**: Store chat conversations for context

**Fields**:
- `user_id` - Who's chatting
- `session_id` - Conversation session
- `message_type` - USER, ASSISTANT, SYSTEM
- `message_text` - The message
- `message_metadata` - Actions taken, data returned
- `timestamp` - When

**Example Use Case**:
```python
# User asks a question
{
  "message_type": "USER",
  "message_text": "Show me unpaid invoices over 30 days",
  "session_id": "chat-session-123"
}

# AI responds
{
  "message_type": "ASSISTANT",
  "message_text": "You have 5 unpaid invoices...",
  "message_metadata": {
    "query_executed": "SELECT ...",
    "results_count": 5,
    "actions": ["generate_report"]
  }
}
```

---

## ⚙️ AI Configuration

**File**: `.env.example`

All AI settings are configurable:

```env
# AI Service Keys
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=your-key
TESSERACT_CMD=/usr/bin/tesseract

# AI Feature Toggles
AI_ENABLED=True
AI_AUTO_CATEGORIZE=True
AI_OCR_ENABLED=True
AI_PREDICTION_ENABLED=True
AI_CHAT_ENABLED=True

# Confidence Thresholds
AI_CATEGORIZATION_THRESHOLD=0.80
AI_OCR_CONFIDENCE_THRESHOLD=0.85
AI_PREDICTION_CONFIDENCE_THRESHOLD=0.75
```

**Available in code**:
```python
from backend.app.core.config import settings

if settings.AI_ENABLED:
    # Use AI features
    pass
```

---

## 📦 AI Dependencies Installed

**File**: `requirements.txt`

Already included:

```
# LLM APIs
openai==1.3.7                  # OpenAI GPT-4
anthropic==0.7.7               # Anthropic Claude
langchain==0.1.0               # LLM orchestration
langchain-openai==0.0.2
langchain-anthropic==0.0.2

# Document Processing
pytesseract==0.3.10            # OCR
pdf2image==1.16.3              # PDF to image
pypdf2==3.0.1                  # PDF parsing
pillow==10.1.0                 # Image processing

# Machine Learning
scikit-learn==1.3.2            # ML models
pandas==2.1.4                  # Data analysis
numpy==1.26.2                  # Numerical computing
prophet==1.1.5                 # Time series forecasting
statsmodels==0.14.1            # Statistical models

# NLP
spacy==3.7.2                   # Natural language processing
transformers==4.35.2           # Hugging Face models
tiktoken==0.5.2                # Token counting
```

---

## 🛠️ How to Implement AI Services

### Step 1: Create AI Service Module

Create `backend/app/services/ai_service.py`:

```python
"""AI Service for document processing, categorization, and predictions."""
from typing import Optional, Dict, Any
import openai
from anthropic import Anthropic
from backend.app.core.config import settings

class AIService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        if settings.ANTHROPIC_API_KEY:
            self.anthropic = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def process_document(self, file_content: bytes, file_type: str) -> Dict[str, Any]:
        """Extract data from invoice/receipt using OCR + GPT-4."""
        # 1. OCR: Extract text using Tesseract
        # 2. Structure: Use GPT-4 to identify fields
        # 3. Validate: Check extracted data
        pass

    async def categorize_transaction(
        self,
        description: str,
        amount: float,
        company_id: str
    ) -> Dict[str, Any]:
        """Suggest account for transaction."""
        # 1. Get historical patterns from ai_training_data
        # 2. Use GPT-4 to suggest account
        # 3. Return suggestion with confidence
        pass

    async def chat(self, message: str, context: Dict[str, Any]) -> str:
        """Chat with AI about accounting data."""
        # 1. Parse user intent
        # 2. Execute database queries if needed
        # 3. Format response
        pass

    async def predict_cash_flow(
        self,
        company_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """Predict cash flow."""
        # 1. Get historical data
        # 2. Get outstanding AR/AP
        # 3. Use Prophet or ARIMA for forecast
        pass
```

### Step 2: Update Endpoints to Use Service

Update `backend/app/api/v1/endpoints/ai_assistant.py`:

```python
from backend.app.services.ai_service import AIService

ai_service = AIService()

@router.post("/process-document")
async def process_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Process document with OCR and AI extraction."""
    file_content = await file.read()

    # Use the AI service
    result = await ai_service.process_document(
        file_content=file_content,
        file_type=file.content_type
    )

    # Save to database
    # ... create bill or expense entry

    return result
```

### Step 3: Implement Training Data Loop

When user corrects a suggestion:

```python
from backend.app.models.ai import AITrainingData

async def save_categorization_feedback(
    description: str,
    suggested_account: str,
    actual_account: str,
    db: AsyncSession
):
    """Store user correction for training."""
    training_data = AITrainingData(
        company_id=company_id,
        data_type="CATEGORIZATION",
        input_data=json.dumps({"description": description}),
        output_data=json.dumps({"account_id": actual_account}),
        is_validated=True,
        confidence_score=1.0
    )
    db.add(training_data)
    await db.commit()
```

---

## 🎯 AI Usage Throughout the App

### **Chart of Accounts**
- AI suggests account names based on business type
- Detects duplicate accounts
- Recommends optimal structure

### **Journal Entries**
- AI suggests entries based on description
- Validates balanced entries
- Flags unusual transactions

### **Invoices/Bills**
- OCR processing of uploaded documents
- Auto-fill customer/vendor details
- Suggest payment terms

### **Bank Reconciliation**
- Auto-match transactions (fuzzy matching)
- Learn from user confirmations
- Flag unmatched items

### **Reports**
- Natural language queries ("Show Q3 revenue")
- AI commentary on results
- Explain variances automatically

### **Dashboard**
- Real-time insights and alerts
- Predictive KPIs
- Anomaly detection

---

## 📝 Example Implementation: Document OCR

Here's a complete example:

```python
# backend/app/services/ai_service.py

import pytesseract
from PIL import Image
import io
import openai
import json

class AIService:
    async def process_document(
        self,
        file_content: bytes,
        file_type: str
    ) -> Dict[str, Any]:
        """Extract invoice data from image/PDF."""

        # Step 1: OCR - Extract text
        image = Image.open(io.BytesIO(file_content))
        text = pytesseract.image_to_string(image)

        # Step 2: Use GPT-4 to structure data
        prompt = f"""
        Extract the following information from this invoice:
        - Vendor name
        - Invoice date
        - Invoice number
        - Total amount
        - Tax amount
        - Line items (description, quantity, price)

        Text from invoice:
        {text}

        Return as JSON.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        # Step 3: Parse and validate
        extracted = json.loads(response.choices[0].message.content)

        return {
            "document_type": "invoice",
            "extracted_data": extracted,
            "confidence": 0.95,
            "raw_text": text
        }
```

---

## ✅ Quick Checklist: Adding AI

- [ ] Get OpenAI API key from https://platform.openai.com
- [ ] Add API key to `.env`
- [ ] Create `backend/app/services/ai_service.py`
- [ ] Implement `process_document()` method
- [ ] Implement `categorize_transaction()` method
- [ ] Implement `chat()` method with LangChain
- [ ] Implement `predict_cash_flow()` with Prophet
- [ ] Update endpoints to use AIService
- [ ] Test with real documents
- [ ] Add training data feedback loop

---

## 🎓 Summary

**What's Ready**:
✅ API endpoints structure
✅ Database tables for AI data
✅ Configuration system
✅ Dependencies installed
✅ Models for storing predictions

**What Needs Implementation**:
⚠️ Actual OpenAI/Anthropic integration
⚠️ OCR processing logic
⚠️ ML model training
⚠️ LangChain chatbot setup
⚠️ Time series forecasting

**Time Estimate**:
- Document OCR: 2-3 days
- Auto-categorization: 2-3 days
- Chat assistant: 3-5 days
- Predictions: 3-5 days
- **Total: 2-3 weeks for full AI integration**

---

## 📚 Next Steps

1. **Start with Document OCR** - Most visible and valuable
2. **Add Auto-Categorization** - Saves tons of time
3. **Implement Chat** - Great user experience
4. **Add Predictions** - Advanced feature

Would you like me to implement any of these AI services for you? I can start with the document OCR or auto-categorization!

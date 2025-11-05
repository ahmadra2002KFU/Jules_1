# Modern AI-Powered Accounting System

A comprehensive, modern accounting application with integrated AI capabilities, built with Python (FastAPI) backend and designed for scalability and ease of use.

## 🚀 Overview

This is a **Proof of Concept (PoC)** for a full-featured accounting system similar to Alshamel, Babel, and Bisan, but enhanced with cutting-edge AI technology. The system supports complete double-entry bookkeeping, financial management, inventory tracking, and intelligent automation through AI.

### Key Features

- ✅ **Complete Accounting Core**: Chart of Accounts, Journal Entries, General Ledger
- ✅ **Accounts Receivable & Payable**: Full AR/AP management with aging reports
- ✅ **Banking & Reconciliation**: Multi-bank account management with AI-powered reconciliation
- ✅ **Inventory Management**: Multi-location inventory with costing methods (FIFO, LIFO, Weighted Average)
- ✅ **Fixed Assets**: Asset tracking with automated depreciation
- ✅ **Financial Reporting**: Balance Sheet, P&L, Cash Flow, Trial Balance, and more
- ✅ **AI-Powered Features**:
  - Document OCR (receipt/invoice scanning)
  - Auto-categorization of transactions
  - Predictive analytics (cash flow, sales forecasting)
  - Natural language query interface
  - Anomaly detection
  - Smart reconciliation
- ✅ **Multi-Currency Support**: Handle transactions in multiple currencies
- ✅ **Multi-Language**: Arabic and English support with RTL
- ✅ **Cost Centers & Projects**: Track costs by department/project
- ✅ **Budgeting**: Create and monitor budgets vs actuals
- ✅ **Tax Management**: VAT, Sales Tax, Withholding Tax
- ✅ **Audit Trail**: Complete audit logging

## 📋 Table of Contents

- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [AI Features](#ai-features)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🏗️ Architecture

### System Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend  │ ◄─────► │   Backend    │ ◄─────► │  Database   │
│   (React)   │         │  (FastAPI)   │         │  (SQLite)   │
└─────────────┘         └──────────────┘         └─────────────┘
                              │
                              ▼
                        ┌──────────────┐
                        │  AI Services │
                        │ (OpenAI/LLM) │
                        └──────────────┘
```

### Database Design

The database follows a comprehensive double-entry accounting structure with 40+ tables including:

- **Core Tables**: Companies, Fiscal Years, Accounting Periods
- **Accounting**: Chart of Accounts, Journal Entries, General Ledger
- **AR/AP**: Customers, Vendors, Invoices, Bills, Payments
- **Banking**: Bank Accounts, Transactions, Reconciliations
- **Inventory**: Items, Warehouses, Stock Levels, Transactions
- **Fixed Assets**: Assets, Depreciation Schedules
- **Configuration**: Cost Centers, Projects, Tax Codes, Currencies
- **AI**: Training Data, Predictions, Chat History
- **Security**: Users, Roles, Permissions, Audit Logs

See [database_schema.sql](database_schema.sql) for complete schema.

## 🛠️ Technology Stack

### Backend

- **Framework**: FastAPI 0.104+ (Python 3.11+)
- **Database**: SQLite (PoC) / PostgreSQL (Production)
- **ORM**: SQLAlchemy 2.0 (Async)
- **Authentication**: JWT tokens with OAuth2
- **Validation**: Pydantic v2
- **API Docs**: Swagger/OpenAPI (auto-generated)

### AI & Machine Learning

- **LLMs**: OpenAI GPT-4, Anthropic Claude
- **Orchestration**: LangChain
- **OCR**: Tesseract, GPT-4 Vision
- **ML Libraries**: scikit-learn, pandas, numpy
- **Forecasting**: Prophet, statsmodels

### Frontend (To be implemented)

- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI or Ant Design
- **State**: Redux Toolkit / Zustand
- **Charts**: Recharts / ECharts
- **i18n**: i18next (Arabic/English)

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- OpenAI API key (for AI features) - optional for basic functionality

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd Jules_1
```

2. **Create and activate virtual environment**

```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=sqlite+aiosqlite:///./accounting.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# AI Configuration (Optional)
OPENAI_API_KEY=sk-your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Application
DEBUG=True
RELOAD=True
```

5. **Initialize the database**

```bash
cd backend
python -m app.db.init_db
```

6. **Run the application**

```bash
# From the backend directory
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. **Access the application**

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
Jules_1/
├── PRD.md                          # Product Requirements Document
├── README.md                       # This file
├── database_schema.sql             # Complete database schema
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (create this)
├── .gitignore                     # Git ignore file
│
├── backend/                       # Backend application
│   ├── app/
│   │   ├── main.py               # FastAPI application entry point
│   │   ├── core/
│   │   │   └── config.py         # Application configuration
│   │   ├── db/
│   │   │   └── base.py           # Database session management
│   │   ├── models/               # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── user.py
│   │   │   ├── company.py
│   │   │   ├── chart_of_accounts.py
│   │   │   ├── journal_entry.py
│   │   │   ├── customer.py
│   │   │   ├── vendor.py
│   │   │   ├── invoice.py
│   │   │   ├── bill.py
│   │   │   ├── payment.py
│   │   │   ├── bank.py
│   │   │   ├── item.py
│   │   │   ├── fixed_asset.py
│   │   │   ├── cost_center.py
│   │   │   ├── budget.py
│   │   │   ├── tax.py
│   │   │   ├── currency.py
│   │   │   ├── payment_terms.py
│   │   │   ├── document.py
│   │   │   ├── ai.py
│   │   │   └── audit.py
│   │   ├── schemas/              # Pydantic schemas (to be implemented)
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── api.py        # Main API router
│   │   │       └── endpoints/    # API endpoints
│   │   │           ├── auth.py
│   │   │           ├── companies.py
│   │   │           ├── chart_of_accounts.py
│   │   │           ├── journal_entries.py
│   │   │           ├── invoices.py
│   │   │           ├── bills.py
│   │   │           ├── payments.py
│   │   │           ├── customers.py
│   │   │           ├── vendors.py
│   │   │           ├── bank_accounts.py
│   │   │           ├── items.py
│   │   │           ├── reports.py
│   │   │           ├── dashboard.py
│   │   │           └── ai_assistant.py
│   │   ├── services/             # Business logic services
│   │   └── utils/                # Utility functions
│   ├── tests/                    # Test suite
│   └── alembic/                  # Database migrations
│
└── frontend/                     # Frontend application (to be implemented)
    ├── public/
    └── src/
        ├── components/
        ├── pages/
        ├── services/
        ├── store/
        ├── utils/
        └── styles/
```

## 📚 API Documentation

### Authentication

```bash
# Login
POST /api/v1/auth/login
{
  "username": "user",
  "password": "password"
}

# Get current user
GET /api/v1/auth/me
Headers: Authorization: Bearer <token>
```

### Chart of Accounts

```bash
# Get all accounts
GET /api/v1/chart-of-accounts/?company_id=<company_id>

# Create account
POST /api/v1/chart-of-accounts/
{
  "company_id": "comp-123",
  "account_code": "1010",
  "account_name_en": "Cash",
  "account_type": "ASSET",
  "account_nature": "DEBIT"
}

# Get account tree
GET /api/v1/chart-of-accounts/tree?company_id=<company_id>
```

### Journal Entries

```bash
# Create journal entry
POST /api/v1/journal-entries/
{
  "company_id": "comp-123",
  "entry_date": "2024-01-01",
  "description": "Opening entry",
  "lines": [
    {
      "account_id": "acc-1",
      "debit_amount": 10000,
      "credit_amount": 0
    },
    {
      "account_id": "acc-2",
      "debit_amount": 0,
      "credit_amount": 10000
    }
  ]
}

# Post journal entry
POST /api/v1/journal-entries/{entry_id}/post
```

### Reports

```bash
# Balance Sheet
GET /api/v1/reports/balance-sheet?company_id=<id>&as_of_date=2024-12-31

# Income Statement
GET /api/v1/reports/income-statement?company_id=<id>&start_date=2024-01-01&end_date=2024-12-31

# Trial Balance
GET /api/v1/reports/trial-balance?company_id=<id>&as_of_date=2024-12-31

# AR Aging
GET /api/v1/reports/ar-aging?company_id=<id>&as_of_date=2024-12-31
```

### AI Assistant

```bash
# Chat with AI
POST /api/v1/ai/chat
{
  "message": "Show me unpaid invoices over 30 days"
}

# Process document (OCR)
POST /api/v1/ai/process-document
Form-data: file=<invoice.pdf>

# Auto-categorize transaction
POST /api/v1/ai/categorize-transaction
{
  "description": "Office rent payment",
  "amount": 1500
}

# Get AI insights
GET /api/v1/ai/insights?company_id=<id>

# Predict cash flow
POST /api/v1/ai/predict/cash-flow?company_id=<id>&days=30
```

For complete API documentation, visit http://localhost:8000/docs after starting the server.

## 🤖 AI Features

### 1. Document Processing (OCR)

Upload receipts or invoices and automatically extract:
- Vendor/Customer information
- Date, amounts, tax
- Line items
- Payment terms

**Example**:
```python
# Upload an invoice image
response = await ai_service.process_document(file)
# Returns: extracted data with 95% confidence
```

### 2. Auto-Categorization

Automatically assign accounts to transactions based on:
- Transaction description
- Historical patterns
- Vendor/Customer
- Amount patterns

**Example**:
```python
transaction = "Office rent - January 2024"
category = await ai_service.categorize(transaction)
# Suggests: "Rent Expense" with 92% confidence
```

### 3. Predictive Analytics

- **Cash Flow Forecasting**: Predict cash position for next 30/60/90 days
- **Sales Forecasting**: Predict future sales trends
- **Expense Prediction**: Forecast upcoming expenses
- **Budget Variance Prediction**: Early warning of budget overruns

### 4. Natural Language Interface

Ask questions in plain English or Arabic:
- "Show me top 10 customers by revenue"
- "What's my cash position?"
- "Generate P&L for Q3 2024"
- "Create journal entry for office rent $1,500"

### 5. Anomaly Detection

AI monitors and alerts on:
- Unusual transactions
- Duplicate entries
- Out-of-pattern expenses
- Potential fraud indicators
- Budget anomalies

### 6. Smart Reconciliation

AI-powered bank reconciliation:
- Auto-matches bank transactions
- Fuzzy matching for similar amounts
- Pattern recognition
- Learns from user confirmations

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_journal_entries.py

# Run with verbose output
pytest -v
```

## 🔧 Development

### Code Quality

```bash
# Format code
black backend/

# Sort imports
isort backend/

# Lint
flake8 backend/

# Type checking
mypy backend/
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🚢 Deployment

### Using Docker (Recommended)

```bash
# Build image
docker build -t accounting-app .

# Run container
docker run -p 8000:8000 accounting-app
```

### Manual Deployment

1. Set up PostgreSQL database
2. Update `.env` with production settings
3. Set `DEBUG=False`
4. Use production WSGI server (Gunicorn)

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## 📈 Roadmap

### Phase 1: Core Accounting (✅ Completed)
- Chart of Accounts
- Journal Entries
- General Ledger
- Basic Reports

### Phase 2: AR/AP & Banking (🚧 In Progress)
- Customer/Vendor management
- Invoices and Bills
- Payment processing
- Bank reconciliation

### Phase 3: Inventory (📋 Planned)
- Item master
- Stock movements
- Inventory valuation

### Phase 4: AI Integration (📋 Planned)
- Document OCR
- Auto-categorization
- Predictive analytics
- AI chatbot

### Phase 5: Frontend (📋 Planned)
- React-based UI
- Dashboard
- Responsive design
- Arabic/English support

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by Alshamel, Babel, and Bisan accounting systems
- Built with FastAPI, SQLAlchemy, and modern Python ecosystem
- AI powered by OpenAI and Anthropic

## 📞 Support

For questions or issues, please:
- Open an issue on GitHub
- Email: support@example.com
- Documentation: See [PRD.md](PRD.md) for detailed specifications

## 🎯 Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
cd backend
python -m app.main

# Access API docs
open http://localhost:8000/docs

# Run tests
pytest

# Format code
black backend/ && isort backend/
```

---

**Built with ❤️ using FastAPI, SQLAlchemy, and AI**

*This is a Proof of Concept (PoC) - suitable for development and testing. For production use, additional security measures and testing are recommended.*

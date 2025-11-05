# Setup Guide

## Quick Setup (Development)

### 1. Prerequisites

Ensure you have the following installed:
- Python 3.11 or higher
- pip (Python package installer)
- git

Optional (for AI features):
- OpenAI API key
- Anthropic API key

### 2. Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd Jules_1

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor

# Minimum required settings for basic functionality:
# - SECRET_KEY (generate with: openssl rand -hex 32)
# - DATABASE_URL (default SQLite works out of the box)

# For AI features, add:
# - OPENAI_API_KEY (get from https://platform.openai.com)
```

### 4. Initialize Database

```bash
# The database will be automatically created on first run
# Or you can initialize it manually:
cd backend
python << 'PYEOF'
import asyncio
from app.db.base import init_db

async def main():
    await init_db()
    print("Database initialized successfully!")

asyncio.run(main())
PYEOF
```

### 5. Run the Application

```bash
# From the backend directory
python -m app.main

# Or use uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access the Application

- **API Root**: http://localhost:8000
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Production Setup

### 1. Database (PostgreSQL)

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE accounting_db;
CREATE USER accounting_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE accounting_db TO accounting_user;
\q

# Update .env
DATABASE_URL=postgresql+asyncpg://accounting_user:secure_password@localhost:5432/accounting_db
```

### 2. Security Configuration

```bash
# Generate secure secret key
openssl rand -hex 32

# Update .env
SECRET_KEY=<generated-key>
DEBUG=False
RELOAD=False
```

### 3. Production Server (Gunicorn)

```bash
# Install Gunicorn (already in requirements.txt)
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

### 4. Using Docker

```dockerfile
# Create Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t accounting-app .
docker run -p 8000:8000 --env-file .env accounting-app
```

### 5. Nginx Reverse Proxy (Optional)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Common Issues

**1. Import Errors**

```bash
# Make sure you're in the backend directory
cd backend

# And run with module syntax
python -m app.main
```

**2. Database Connection Errors**

```bash
# For SQLite, ensure the directory is writable
chmod 755 .

# For PostgreSQL, check connection string
# Ensure PostgreSQL is running
sudo systemctl status postgresql
```

**3. AI Features Not Working**

```bash
# Check API keys in .env
echo $OPENAI_API_KEY

# Verify AI is enabled
AI_ENABLED=True
```

**4. Port Already in Use**

```bash
# Find process using port 8000
lsof -i :8000

# Kill it or use a different port
uvicorn app.main:app --port 8001
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit files in your preferred editor.

### 3. Format Code

```bash
# Format with Black
black backend/

# Sort imports
isort backend/

# Check linting
flake8 backend/
```

### 4. Run Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app tests/
```

### 5. Commit Changes

```bash
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

## Next Steps

1. **Explore API Documentation**: Visit http://localhost:8000/docs
2. **Read the PRD**: See [PRD.md](PRD.md) for detailed specifications
3. **Check Examples**: Review endpoint files in `backend/app/api/v1/endpoints/`
4. **Implement Features**: Start with core accounting modules
5. **Add AI Features**: Integrate OpenAI for document processing

## Support

For issues or questions:
- Check the [README.md](README.md)
- Review [PRD.md](PRD.md)
- Open an issue on GitHub

Happy coding! 🚀

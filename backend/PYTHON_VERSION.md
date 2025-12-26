# Python Version Compatibility

## Important Note

**Python 3.14 is very new** and many ML/AI packages (TensorFlow, PyTorch, etc.) don't support it yet.

## Recommended Python Versions

For best compatibility, use:
- **Python 3.11** (recommended)
- **Python 3.12** (also good)

These versions are stable and fully supported by all packages in this project.

## If You're Using Python 3.14

Some packages may not install. You have two options:

### Option 1: Use Python 3.11 or 3.12 (Recommended)

```bash
# Install Python 3.11 via Homebrew
brew install python@3.11

# Create new virtual environment with Python 3.11
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Option 2: Install Core Packages Only (Python 3.14)

The core application will work without TensorFlow/PyTorch. You can:

1. Install core requirements (without ML packages):
```bash
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary asyncpg redis pydantic pydantic-settings python-jose passlib python-multipart httpx playwright beautifulsoup4 lxml python-dotenv pytest pytest-asyncio celery flower websockets boto3 chromadb
```

2. The property analysis service will use fallback heuristics instead of ResNet50
3. The chatbot will use fallback responses instead of DialoGPT

## Checking Your Python Version

```bash
python --version
# or
python3 --version
```

## Creating a New Virtual Environment

If you need to switch Python versions:

```bash
# Remove old venv
rm -rf backend/venv

# Create new venv with specific Python version
cd backend
python3.11 -m venv venv  # or python3.12
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```


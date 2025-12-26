# Quick Start Guide

## Prerequisites Installation

### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.10+
brew install python@3.10

# Install Node.js 18+
brew install node@18

# Install Docker Desktop
brew install --cask docker

# Install PostgreSQL
brew install postgresql@14
brew services start postgresql@14

# Install Redis
brew install redis
brew services start redis
```

### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install Python 3.10+
sudo apt install python3.10 python3.10-venv python3-pip

# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Docker
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# Install PostgreSQL
sudo apt install postgresql-14
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Install Redis
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

## Step-by-Step Setup

### 1. Clone and Navigate
```bash
cd RealEstate-AI
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your settings (at minimum, set database URL)
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/realestate_ai

# Create database
createdb realestate_ai  # Or use psql: CREATE DATABASE realestate_ai;

# Run migrations (optional - tables auto-create on first run)
# alembic upgrade head

# Start backend server
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000
API docs at: http://localhost:8000/docs

### 3. Frontend Setup (New Terminal)
```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:3000

### 4. Train ML Model (Optional)
```bash
cd ml_models
python train_lead_scoring.py
```

This will generate a trained model at `ml_models/lead_scoring_model.pkl`

## Using Docker Compose (Alternative)

```bash
# From project root
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## First Login

1. Open http://localhost:3000
2. Click "Register" to create an account
3. Enter email, password, and full name
4. You'll be automatically logged in

## Testing the API

### Using Postman
1. Import `docs/api.postman_collection.json` into Postman
2. Set `base_url` variable to `http://localhost:8000`
3. Register a new user
4. Login to get `access_token`
5. Set `access_token` variable
6. Test other endpoints

### Using curl
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123"

# Use the access_token from login response
curl -X GET http://localhost:8000/api/v1/leads \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Key Features to Test

1. **Lead Management**: Create leads, view pipeline, update status
2. **List Stacking**: Search properties using public records
3. **Chatbot**: Start conversations with leads
4. **Property Analysis**: Upload images for AI analysis
5. **Cash Buyers**: Scrape and search for cash buyers
6. **No-Code Builder**: Generate tools from descriptions

## Troubleshooting

### Backend won't start
- Check if PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in .env
- Check port 8000 is not in use: `lsof -i :8000`

### Frontend can't connect
- Verify backend is running on port 8000
- Check NEXT_PUBLIC_API_URL in .env.local
- Check browser console for errors

### Database connection errors
- Ensure PostgreSQL is running
- Verify database exists: `psql -l | grep realestate_ai`
- Check DATABASE_URL format: `postgresql://user:password@host:port/database`

### ML models not loading
- Run training script first: `python ml_models/train_lead_scoring.py`
- Models will use fallback algorithms if not found

## Next Steps

- Read `docs/deployment.md` for production deployment
- Review API documentation at http://localhost:8000/docs
- Explore the codebase structure
- Customize models and services for your needs


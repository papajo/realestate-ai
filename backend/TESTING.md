# Testing the API

## Method 1: Interactive Swagger UI (Recommended)

FastAPI automatically provides an interactive browser-based API documentation:

1. Start the server:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. Open your browser and visit:
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

3. In Swagger UI, you can:
   - See all available endpoints
   - Click "Try it out" on any endpoint
   - Fill in parameters
   - Execute requests
   - See responses directly in the browser

## Method 2: Test Script

Run the automated test script:

```bash
cd backend
source venv/bin/activate
python test_api.py
```

This will test:
- Health endpoint
- Root endpoint
- User registration
- User login
- Authenticated endpoints (leads, list stacking, etc.)

## Method 3: Using curl

### Health Check
```bash
curl http://localhost:8000/health
```

### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123"
```

### Get Current User (with token)
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Method 4: Using Python Requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Register
response = requests.post(
    "http://localhost:8000/api/v1/auth/register",
    json={"email": "test@example.com", "password": "test123", "full_name": "Test User"}
)
print(response.json())

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    data={"username": "test@example.com", "password": "test123"}
)
token = response.json()["access_token"]

# Authenticated request
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/api/v1/leads", headers=headers)
print(response.json())
```

## Method 5: Postman Collection

Import the Postman collection:
- File: `docs/api.postman_collection.json`
- Import into Postman
- Set `base_url` variable to `http://localhost:8000`
- Set `access_token` after logging in

## Quick Test Checklist

- [ ] Server is running (`uvicorn app.main:app --reload`)
- [ ] Health endpoint works: http://localhost:8000/health
- [ ] Swagger UI accessible: http://localhost:8000/docs
- [ ] Can register a user
- [ ] Can login and get token
- [ ] Can access authenticated endpoints

## Troubleshooting

### "Connection refused"
- Make sure the server is running
- Check the port (default: 8000)

### "Database connection error"
- Set up PostgreSQL (see `DATABASE_SETUP.md`)
- Or the app will start but database endpoints won't work

### "401 Unauthorized"
- Make sure you're including the Bearer token in the Authorization header
- Token might be expired, try logging in again


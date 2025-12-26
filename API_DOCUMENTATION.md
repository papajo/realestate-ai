# API Documentation - RealEstate-AI

## Overview
Complete REST API documentation for the AI Real Estate Investing platform.

## Base URL
- Development: `http://localhost:8000/api/v1`
- Production: `https://api.realestate-ai.com/api/v1`

## Authentication
All API requests (except `/auth/register` and `/auth/login`) require JWT Bearer token.

```bash
Authorization: Bearer <your_access_token>
```

---

## Authentication Endpoints

### Register User
**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2025-12-26T23:14:25.745155Z"
}
```

**Error Responses:**
- `400 Bad Request`: Email already registered
- `422 Unprocessable Entity`: Invalid input data

---

### Login
**POST** `/auth/login`

Authenticate user and receive JWT tokens.

**Request Body (form-urlencoded):**
```
username=user@example.com&password=SecurePassword123!
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized`: Incorrect email or password

---

### Get Current User
**GET** `/auth/me`

Get the authenticated user's profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2025-12-26T23:14:25.745155Z"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token

---

### Refresh Token
**POST** `/auth/refresh`

Get a new access token using refresh token.

**Request Body (JSON):**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## Lead Management Endpoints

### Create Lead
**POST** `/leads/`

Create a new real estate lead.

**Request Body:**
```json
{
  "property_address": "123 Main Street",
  "property_city": "Portland",
  "property_state": "OR",
  "property_zip": "97201",
  "owner_name": "Jane Smith",
  "owner_email": "jane@example.com",
  "owner_phone": "555-1234"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": 1,
  "property_address": "123 Main Street",
  "property_city": "Portland",
  "property_state": "OR",
  "property_zip": "97201",
  "owner_name": "Jane Smith",
  "owner_email": "jane@example.com",
  "owner_phone": "555-1234",
  "lead_score": 0.0,
  "distress_signals": {},
  "status": "new",
  "source": "manual",
  "created_at": "2025-12-26T23:30:00Z",
  "updated_at": null
}
```

---

### Get All Leads
**GET** `/leads/`

Retrieve all leads for the authenticated user.

**Query Parameters:**
```
skip=0          # Number of records to skip (default: 0)
limit=100       # Number of records to return (default: 100, max: 1000)
status_filter=new   # Filter by lead status (optional)
min_score=5.0   # Filter by minimum lead score (optional)
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "property_address": "123 Main Street",
    "property_city": "Portland",
    "property_state": "OR",
    "property_zip": "97201",
    "owner_name": "Jane Smith",
    "lead_score": 0.0,
    "status": "new",
    "source": "manual",
    "created_at": "2025-12-26T23:30:00Z"
  }
]
```

---

### Get Single Lead
**GET** `/leads/{lead_id}`

Retrieve details of a specific lead.

**Path Parameters:**
- `lead_id` (integer): The ID of the lead

**Response (200 OK):**
```json
{
  "id": 1,
  "property_address": "123 Main Street",
  "property_city": "Portland",
  "property_state": "OR",
  "property_zip": "97201",
  "owner_name": "Jane Smith",
  "lead_score": 0.0,
  "status": "new",
  "source": "manual",
  "created_at": "2025-12-26T23:30:00Z"
}
```

**Error Responses:**
- `404 Not Found`: Lead not found

---

### Update Lead
**PATCH** `/leads/{lead_id}`

Update a lead's status or scoring.

**Request Body:**
```json
{
  "status": "qualified",
  "lead_score": 85.5,
  "distress_signals": {
    "property_condition": "poor",
    "financial_stress": true
  }
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "property_address": "123 Main Street",
  "status": "qualified",
  "lead_score": 85.5,
  "distress_signals": {
    "property_condition": "poor",
    "financial_stress": true
  }
}
```

---

## Health Check

### Health Status
**GET** `/health`

Check if the API is operational.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Invalid data format
- `500 Internal Server Error`: Server error

---

## Rate Limiting

API requests are rate-limited to prevent abuse:
- **General API**: 100 requests per minute
- **Authentication**: 10 requests per minute

Rate limit headers in response:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640596200
```

---

## Data Types

### Lead Status
- `new`: Newly created lead
- `qualified`: Meets investment criteria
- `contacted`: Contacted the property owner
- `converted`: Turned into a deal
- `lost`: No longer interested

### Lead Source
- `manual`: Manually entered
- `list_stacking`: From list stacking service
- `referral`: Referred by another user

---

## Examples

### Complete Workflow

#### 1. Register
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "investor@example.com",
    "password": "SecurePassword123!",
    "full_name": "Real Estate Investor"
  }'
```

#### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=investor@example.com&password=SecurePassword123!'
```

Save the `access_token` from the response.

#### 3. Create Lead
```bash
curl -X POST http://localhost:8000/api/v1/leads/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "property_address": "456 Oak Ave",
    "property_city": "Seattle",
    "property_state": "WA",
    "property_zip": "98101",
    "owner_name": "John Owner",
    "owner_email": "john@example.com",
    "owner_phone": "206-555-0123"
  }'
```

#### 4. Get Leads
```bash
curl -X GET http://localhost:8000/api/v1/leads/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## Interactive API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

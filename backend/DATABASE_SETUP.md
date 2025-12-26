# Database Setup Guide

## Quick Setup (macOS with Homebrew)

### 1. Install PostgreSQL

```bash
brew install postgresql@14
brew services start postgresql@14
```

### 2. Create Database and User

```bash
# Connect to PostgreSQL
psql postgres

# In PostgreSQL prompt, run:
CREATE DATABASE realestate_ai;
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER USER postgres WITH SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE realestate_ai TO postgres;
\q
```

### 3. Update .env File

Make sure your `backend/.env` file has:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/realestate_ai
```

### 4. Restart the Server

The app will automatically create tables on startup.

## Alternative: Use Docker PostgreSQL

If you prefer using Docker:

```bash
# Start PostgreSQL in Docker
docker run --name postgres-realestate \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=realestate_ai \
  -p 5432:5432 \
  -d postgres:14-alpine

# Your DATABASE_URL stays the same:
# postgresql://postgres:postgres@localhost:5432/realestate_ai
```

## Verify Connection

```bash
# Test connection
psql -U postgres -d realestate_ai -c "SELECT version();"
```

## Troubleshooting

### "role postgres does not exist"

Create the user:
```bash
psql postgres
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER USER postgres WITH SUPERUSER;
```

### "database realestate_ai does not exist"

Create the database:
```bash
createdb realestate_ai
# or
psql postgres -c "CREATE DATABASE realestate_ai;"
```

### Connection refused

Make sure PostgreSQL is running:
```bash
# macOS
brew services start postgresql@14

# Linux
sudo systemctl start postgresql

# Check status
pg_isready
```

## Database Schema and Architecture

### Overview

The application uses PostgreSQL with SQLAlchemy ORM for database operations. The schema is designed to support:
- User authentication and authorization
- Lead management and scoring
- AI-powered conversations
- Property analysis results
- Cash buyer database with vector search

### Entity Relationship Diagram

```
┌─────────────┐
│    Users    │
│─────────────│
│ id (PK)     │
│ email       │◄────┐
│ password    │     │
│ full_name   │     │
│ is_active   │     │
│ is_admin    │     │
└─────────────┘     │
                     │
┌─────────────┐     │
│    Leads    │     │
│─────────────│     │
│ id (PK)     │     │
│ user_id (FK)├─────┘
│ address     │
│ city        │
│ state       │
│ zip         │
│ lead_score  │
│ status      │
└─────────────┘
      │
      ├──────────────┬──────────────────┐
      │              │                  │
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│Conversations│ │  Property   │ │ Cash Buyers │
│─────────────│ │  Analyses   │ │─────────────│
│ id (PK)     │ │─────────────│ │ id (PK)     │
│ lead_id (FK)│ │ id (PK)     │ │ name        │
│ user_id (FK)│ │ lead_id(FK) │ │ email       │
│ messages    │ │ issues      │ │ city        │
│ status      │ │ cost_est    │ │ embedding   │
└─────────────┘ └─────────────┘ └─────────────┘
```

### Tables

#### 1. `users`
User accounts and authentication.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Primary key |
| email | VARCHAR | Unique email address (indexed) |
| hashed_password | VARCHAR | Bcrypt hashed password |
| full_name | VARCHAR | User's full name |
| is_active | BOOLEAN | Account active status |
| is_admin | BOOLEAN | Administrator privileges |
| encrypted_phone | TEXT | Encrypted phone number (AWS KMS) |
| encrypted_address | TEXT | Encrypted address (AWS KMS) |
| created_at | TIMESTAMP | Account creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

**Indexes:**
- `email` (unique)

#### 2. `leads`
Real estate leads/properties.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Primary key |
| user_id | INTEGER (FK) | Owner user ID → users.id |
| property_address | VARCHAR | Property street address (indexed) |
| property_city | VARCHAR | City |
| property_state | VARCHAR | State |
| property_zip | VARCHAR | ZIP code |
| owner_name | TEXT | Encrypted owner name |
| owner_email | TEXT | Encrypted owner email |
| owner_phone | TEXT | Encrypted owner phone |
| lead_score | FLOAT | AI-calculated lead score (0-1) (indexed) |
| distress_signals | JSON | Detected distress indicators |
| status | VARCHAR | Lead status: new, qualified, contacted, converted, lost |
| source | VARCHAR | Lead source: list_stacking, manual, referral |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

**Indexes:**
- `property_address`
- `lead_score`

**Relationships:**
- One-to-many with `conversations`
- One-to-many with `property_analyses`

#### 3. `conversations`
AI chatbot conversations with leads.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Primary key |
| lead_id | INTEGER (FK) | Associated lead → leads.id |
| user_id | INTEGER (FK) | Owner user → users.id |
| messages | JSON | Array of conversation messages |
| qualification_status | VARCHAR | pending, qualified, not_qualified |
| qualification_score | FLOAT | Qualification confidence (0-1) |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

**Relationships:**
- Many-to-one with `leads`

#### 4. `property_analyses`
Computer vision analysis results.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Primary key |
| lead_id | INTEGER (FK) | Associated lead → leads.id |
| detected_issues | JSON | Array of detected property issues |
| repair_cost_estimate | FLOAT | Total estimated repair cost |
| images_analyzed | INTEGER | Number of images processed |
| created_at | TIMESTAMP | Analysis timestamp |

**Relationships:**
- Many-to-one with `leads`

#### 5. `cash_buyers`
Cash buyer database for matching.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Primary key |
| name | VARCHAR | Buyer name |
| company_name | VARCHAR | Company name (optional) |
| email | TEXT | Encrypted email |
| phone | TEXT | Encrypted phone |
| city | VARCHAR | Location city |
| state | VARCHAR | Location state |
| zip_code | VARCHAR | ZIP code |
| preferred_property_types | JSON | Array of property types |
| price_range_min | FLOAT | Minimum purchase price |
| price_range_max | FLOAT | Maximum purchase price |
| investment_areas | JSON | Array of target areas |
| total_purchases | INTEGER | Historical purchase count |
| average_purchase_price | FLOAT | Average deal size |
| last_purchase_date | TIMESTAMP | Most recent purchase |
| embedding | JSON | Vector embedding for similarity search |
| source | VARCHAR | Data source: scraper, manual |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### Security Features

1. **Password Hashing**: Bcrypt with 12 rounds
2. **PII Encryption**: AWS KMS encryption for sensitive fields
3. **JWT Authentication**: Access and refresh tokens
4. **Database Indexing**: Optimized queries on frequently accessed fields

### Data Flow

1. **Lead Generation**: List stacking → Lead creation → Scoring → Storage
2. **Lead Qualification**: Chatbot conversation → Qualification scoring → Status update
3. **Property Analysis**: Image upload → CV analysis → Issue detection → Cost estimation
4. **Buyer Matching**: Buyer scraping → Vector embedding → Similarity search → Matching

### Migration Strategy

Tables are auto-created on first startup via SQLAlchemy. For production:

```bash
# Generate migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

### Performance Considerations

- **Indexes**: Email, property_address, lead_score
- **JSON Fields**: Used for flexible schema (distress_signals, messages, etc.)
- **Vector Search**: ChromaDB for cash buyer similarity (separate from PostgreSQL)
- **Connection Pooling**: SQLAlchemy connection pool configured

### Backup and Recovery

```bash
# Backup
pg_dump -U postgres realestate_ai > backup.sql

# Restore
psql -U postgres realestate_ai < backup.sql
```


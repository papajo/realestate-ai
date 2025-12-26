# AI Real Estate Investing Scaling Success with Automation

A full-stack SaaS application that leverages AI to automate and optimize real estate investing workflows.

## Features

- **Lead Generation & Analysis**: List stacking with public records, predictive lead scoring
- **AI Chatbot**: NLP-driven lead qualification using Hugging Face DialoGPT
- **Property Analysis**: Computer vision for issue detection and repair cost estimation
- **Cash Buyer Scraping**: Automated buyer identification with vector search
- **No-Code Tool Builder**: Conversational app creation with AI code generation
- **Real-Time Dashboard**: Charts, metrics, and WebSocket notifications

## Architecture

```
├── backend/          # FastAPI backend services
├── frontend/         # Next.js React frontend
├── ml_models/        # ML model training and inference
├── infrastructure/   # Docker, Kubernetes, CI/CD configs
├── monitoring/       # Prometheus, Grafana configs
└── docs/            # Documentation and API specs
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 6+

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Docker Deployment

```bash
docker-compose up -d
```

## Environment Variables

See `.env.example` files in backend and frontend directories.

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

See `docs/deployment.md` for detailed deployment instructions.

## Security

- JWT authentication with refresh tokens
- AWS KMS encryption for PII
- OWASP ZAP vulnerability scanning
- TLS 1.3 encryption in transit

## Project Structure

```
RealEstate-AI/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core config, security, database
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic services
│   │   └── websocket/      # WebSocket handlers
│   ├── alembic/            # Database migrations
│   ├── tests/              # Test files
│   └── requirements.txt    # Python dependencies
├── frontend/                # Next.js frontend
│   ├── app/                # Next.js app directory
│   ├── components/         # React components
│   ├── hooks/              # Custom React hooks
│   └── package.json        # Node dependencies
├── ml_models/              # ML model training
│   ├── train_lead_scoring.py
│   └── sample_data.csv
├── infrastructure/         # Infrastructure as code
│   └── kubernetes/         # K8s deployment configs
├── monitoring/             # Monitoring configs
│   └── prometheus.yml
├── docs/                   # Documentation
│   ├── deployment.md
│   └── api.postman_collection.json
└── docker-compose.yml      # Local development setup
```

## Key Technologies

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **XGBoost**: Machine learning for lead scoring
- **TensorFlow**: Computer vision for property analysis
- **Hugging Face**: NLP for chatbot
- **Playwright**: Web scraping for cash buyers
- **ChromaDB**: Vector database for similarity search

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Data visualization
- **Monaco Editor**: Code editor component
- **React DnD**: Drag-and-drop functionality

### Infrastructure
- **Docker**: Containerization
- **Kubernetes**: Orchestration
- **GCP**: Cloud platform
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **GitHub Actions**: CI/CD

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user

### Leads
- `GET /api/v1/leads` - List leads
- `POST /api/v1/leads` - Create lead
- `GET /api/v1/leads/{id}` - Get lead details
- `PATCH /api/v1/leads/{id}` - Update lead
- `DELETE /api/v1/leads/{id}` - Delete lead

### List Stacking
- `POST /api/v1/list-stacking/search` - Search properties
- `POST /api/v1/list-stacking/batch-search` - Batch search

### Chatbot
- `POST /api/v1/chatbot/conversation` - Create/send message
- `GET /api/v1/chatbot/conversation/{lead_id}` - Get conversation
- `GET /api/v1/chatbot/conversations` - List conversations

### Property Analysis
- `POST /api/v1/property-analysis/analyze/{lead_id}` - Analyze images
- `GET /api/v1/property-analysis/{lead_id}` - Get analysis

### Cash Buyers
- `GET /api/v1/cash-buyers` - List buyers
- `POST /api/v1/cash-buyers/scrape` - Scrape new buyers
- `POST /api/v1/cash-buyers/search-similar` - Similarity search

### Tools
- `POST /api/v1/tools/generate` - Generate tool from description
- `GET /api/v1/tools/list` - List user tools
- `GET /api/v1/tools/{id}` - Get tool details

## Development Workflow

1. **Local Development**: Use Docker Compose or run services individually
2. **Testing**: Run `pytest` for backend, `npm test` for frontend
3. **Code Quality**: Follow PEP 8 for Python, ESLint for TypeScript
4. **Git Workflow**: Feature branches, PR reviews, merge to main
5. **CI/CD**: Automatic testing and deployment on push to main

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Submit a pull request
5. Address review feedback

## License

Proprietary - All Rights Reserved


# Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- Kubernetes cluster (for production)
- GCP account with billing enabled (for GKE)
- PostgreSQL database
- Redis instance

## Local Development

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Run migrations (if using Alembic)
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### 2. Frontend Setup

```bash
cd frontend
npm install

# Copy environment file
cp .env.example .env.local
# Edit .env.local with your API URL

# Start development server
npm run dev
```

### 3. Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Production Deployment on GCP

### 1. Build and Push Docker Images

```bash
# Backend
cd backend
docker build -t gcr.io/PROJECT_ID/realestate-backend:latest .
docker push gcr.io/PROJECT_ID/realestate-backend:latest

# Frontend
cd frontend
docker build -t gcr.io/PROJECT_ID/realestate-frontend:latest .
docker push gcr.io/PROJECT_ID/realestate-frontend:latest
```

### 2. Create GKE Cluster

```bash
gcloud container clusters create realestate-cluster \
  --num-nodes=3 \
  --machine-type=n1-standard-2 \
  --zone=us-central1-a
```

### 3. Deploy to Kubernetes

```bash
# Apply configurations
kubectl apply -f infrastructure/kubernetes/

# Create secrets
kubectl create secret generic db-secret --from-literal=url=postgresql://...
kubectl create secret generic redis-secret --from-literal=url=redis://...
kubectl create secret generic jwt-secret --from-literal=secret=your-secret-key
```

### 4. Set Up Monitoring

```bash
# Deploy Prometheus
kubectl apply -f monitoring/prometheus/

# Deploy Grafana
kubectl apply -f monitoring/grafana/
```

## CI/CD Pipeline

The GitHub Actions workflow automatically:
1. Runs tests on push/PR
2. Builds Docker images
3. Pushes to GCR
4. Deploys to GKE (on main branch)

Configure secrets in GitHub:
- `GCP_PROJECT_ID`
- `GKE_CLUSTER_NAME`
- `GKE_ZONE`

## Environment Variables

### Backend

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `JWT_SECRET_KEY`: Secret for JWT tokens
- `JWT_REFRESH_SECRET_KEY`: Secret for refresh tokens
- `AWS_KMS_KEY_ID`: AWS KMS key for encryption
- `HUGGINGFACE_API_KEY`: Hugging Face API key

### Frontend

- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_WS_URL`: WebSocket URL

## Security Checklist

- [ ] Change default JWT secrets
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Set up AWS KMS for encryption
- [ ] Run OWASP ZAP scans
- [ ] Enable database backups
- [ ] Set up log aggregation
- [ ] Configure firewall rules

## Scaling

- Backend: Horizontal scaling via Kubernetes replicas
- Frontend: CDN for static assets
- Database: Read replicas for read-heavy workloads
- Redis: Cluster mode for high availability

## Monitoring

- Prometheus: Metrics collection
- Grafana: Dashboards and visualization
- ELK Stack: Log aggregation (configure separately)

## Troubleshooting

### Backend won't start
- Check database connection
- Verify environment variables
- Check logs: `docker-compose logs backend`

### Frontend can't connect to backend
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings
- Ensure backend is running

### Database connection errors
- Verify DATABASE_URL format
- Check network connectivity
- Ensure database is accessible


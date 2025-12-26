# Production Deployment Guide

## Docker Compose Deployment (Development/Staging)

### Quick Start

```bash
# Clone the repository
git clone <repo-url>
cd RealEstate-AI

# Create .env file with production values
cat > .env << EOF
# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/realestate_ai

# Redis
REDIS_URL=redis://redis:6379/0

# JWT Secrets (CHANGE THESE IN PRODUCTION!)
JWT_SECRET_KEY=$(openssl rand -hex 32)
JWT_REFRESH_SECRET_KEY=$(openssl rand -hex 32)

# AWS KMS (optional)
AWS_KMS_KEY_ID=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# API Keys (optional)
HUGGINGFACE_API_KEY=

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
EOF

# Build and start services
docker-compose up -d

# Check services
docker-compose ps
```

### Database Initialization

```bash
# Run migrations (if needed)
docker-compose exec backend alembic upgrade head

# Create initial user (optional)
docker-compose exec backend python setup_db.py
```

### Verify Deployment

```bash
# Backend health
curl http://localhost:8000/

# Frontend
open http://localhost:3000

# API Documentation
open http://localhost:8000/docs

# Prometheus Metrics
open http://localhost:9090

# Grafana Dashboards
open http://localhost:3001  # admin/admin
```

---

## Kubernetes Deployment (Production)

### Prerequisites

- Kubernetes cluster (v1.20+)
- kubectl configured
- Docker images pushed to registry
- PostgreSQL and Redis services (external or in-cluster)

### Setup Steps

1. **Create namespace**
```bash
kubectl create namespace realestate-ai
```

2. **Create secrets**
```bash
kubectl create secret generic db-credentials \
  --from-literal=DATABASE_URL=postgresql://user:password@postgres:5432/realestate_ai \
  --from-literal=JWT_SECRET_KEY=$(openssl rand -hex 32) \
  --from-literal=JWT_REFRESH_SECRET_KEY=$(openssl rand -hex 32) \
  -n realestate-ai
```

3. **Deploy backend**
```bash
kubectl apply -f infrastructure/kubernetes/backend-deployment.yaml -n realestate-ai
kubectl apply -f infrastructure/kubernetes/backend-service.yaml -n realestate-ai
```

4. **Deploy frontend**
```bash
kubectl apply -f infrastructure/kubernetes/frontend-deployment.yaml -n realestate-ai
kubectl apply -f infrastructure/kubernetes/frontend-service.yaml -n realestate-ai
```

5. **Verify deployments**
```bash
kubectl get deployments -n realestate-ai
kubectl get pods -n realestate-ai
kubectl get services -n realestate-ai
```

### Scaling

```bash
# Scale backend
kubectl scale deployment backend --replicas=3 -n realestate-ai

# Scale frontend
kubectl scale deployment frontend --replicas=2 -n realestate-ai

# Monitor
kubectl logs -f deployment/backend -n realestate-ai
```

---

## Production Checklist

- [ ] Change all default secrets and keys
- [ ] Set up external PostgreSQL (RDS, CloudSQL, etc.)
- [ ] Set up external Redis (ElastiCache, Memorystore, etc.)
- [ ] Configure AWS KMS for encryption (if using)
- [ ] Set up SSL/TLS certificates
- [ ] Configure domain names
- [ ] Enable logging and monitoring
- [ ] Set up automated backups
- [ ] Configure CI/CD pipeline
- [ ] Review and update CORS origins
- [ ] Enable rate limiting
- [ ] Set up alerting and notifications

---

## Monitoring & Logs

### Prometheus Metrics
Access at: `http://<host>:9090`

Key metrics:
- `http_request_duration_seconds`
- `http_requests_total`
- `database_connection_pool_size`

### Grafana Dashboards
Access at: `http://<host>:3001`

Default credentials: `admin:admin`

### Application Logs
```bash
# Docker Compose
docker-compose logs -f backend
docker-compose logs -f frontend

# Kubernetes
kubectl logs -f deployment/backend -n realestate-ai
kubectl logs -f deployment/frontend -n realestate-ai
```

---

## Security Considerations

1. **Database**: Use strong passwords, enable SSL connections
2. **JWT**: Rotate secrets periodically
3. **CORS**: Restrict to known origins only
4. **Rate Limiting**: Enable on production
5. **SSL/TLS**: Use certificates from trusted CAs
6. **Backup**: Regular automated backups
7. **Secrets Management**: Use external secret managers (AWS Secrets Manager, HashiCorp Vault)

---

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Verify database connection
docker-compose exec backend psql $DATABASE_URL -c "SELECT 1"
```

### Frontend won't connect to API
```bash
# Verify API_URL environment variable
docker-compose exec frontend env | grep NEXT_PUBLIC_API_URL

# Check backend is running
curl http://backend:8000/
```

### Database connection issues
```bash
# Check PostgreSQL
docker-compose exec postgres psql -U postgres -l

# Reset database
docker-compose down -v
docker-compose up -d postgres
docker-compose up -d backend
```

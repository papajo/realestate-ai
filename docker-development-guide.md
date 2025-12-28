Docker Development Guide for RealEstate-AI
Here's your complete guide to developing with Docker for this RealEstate-AI project:

🏗️ Current Docker Architecture
Your project has these services:

postgres: Database (port 5432)
redis: Cache (port 6379)
backend: FastAPI app (port 8000)
frontend: Next.js app (port 3000)
prometheus: Monitoring (port 9090)
grafana: Dashboards (port 3001)
🚀 Development Workflow with Docker
1. Start All Services
2. Check Service Status
3. Backend Development
For FastAPI changes:

Debug backend issues:

4. Frontend Development
For React/Next.js changes:

Frontend rebuild triggers:

Changing API endpoints
Adding new environment variables
Modifying package.json
Changing build-time configurations
5. Database Development
Access PostgreSQL:

Reset database:

6. Common Development Tasks
Add New Dependencies
Environment Variables
Debug Network Issues
View Running Processes
🔧 Troubleshooting Guide
"Unable to connect to server" Error
Check if services are running: docker-compose ps
Hard refresh browser: Ctrl+Shift+R (cache issue)
Verify API connectivity:
Rebuild frontend if needed:
Backend Not Starting
Frontend Build Issues
Database Connection Issues
📝 Development Best Practices
1. Volume Mounting
Backend and frontend use volume mounts for live development
Changes reflect immediately without rebuilds
2. Service Dependencies
Services start in correct order (postgres/redis → backend → frontend)
Use depends_on with health checks
3. Environment Variables
Runtime env vars work for backend
Frontend needs build-time env vars for Next.js
4. Caching Strategy
Use --no-cache when debugging build issues
Clear browser cache when testing frontend changes
5. Logs & Debugging
🎯 Quick Commands Reference
🚨 When to Rebuild vs Restart
Just Restart (fast):

Code changes (backend/frontend use volume mounts)
Configuration changes
Environment variable changes
Rebuild Required:

New dependencies (requirements.txt, package.json)
Dockerfile changes
System dependency changes
Frontend API URL changes
Now you can develop independently! The key insight is understanding when Docker needs to rebuild vs just restart. Most development changes will work with just docker-compose up -d after your initial setup.


pwd && ls -la
docker --version && docker-compose --version
docker-compose up -d postgres redis
docker-compose ps postgres redis
docker-compose up -d backend
docker-compose ps backend
sleep 3 && curl -s http://localhost:8000/docs | head -5
curl -s -I http://localhost:8000 | head -3
docker-compose logs backend | tail -10
curl -s http://localhost:8000/api/v1/auth/login -X POST -d "username=test&password=test" -H "Content-Type: application/x-www-form-urlencoded"
docker-compose up -d frontend
docker-compose ps frontend
sleep 3 && curl -s http://localhost:3000 | grep -o "AI Real Estate Investing"
docker-compose ps
docker-compose exec frontend curl -s http://backend:8000/api/v1/auth/login -X POST -d "username=test&password=test" -H "Content-Type: application/x-www-form-urlencoded"
docker-compose exec frontend grep -r "http://backend:8000" /app/.next/ | head -1
http://localhost:3000

docker-compose logs -f backend

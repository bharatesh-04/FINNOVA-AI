# DEPLOYMENT.md - Finnova AI Deployment Guide

## Deployment Options

### Option 1: Docker Compose (Local/Self-Hosted)

#### Prerequisites
- Docker and Docker Compose installed
- PostgreSQL 15+
- Redis
- Ollama (optional, for AI features)

#### Steps

1. **Clone and Setup**
```bash
git clone <repository>
cd FINNOVA-AI
cp backend/.env.example backend/.env
```

2. **Configure Environment**
Edit `backend/.env`:
```
DATABASE_URL=postgresql://user:password@postgres:5432/finnova_ai_db
REDIS_URL=redis://redis:6379/0
SECRET_KEY=<generate-secure-key>
```

3. **Deploy**
```bash
docker-compose up -d
```

4. **Access**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### Option 2: Vercel + Railway

#### Frontend Deployment (Vercel)

1. **Connect Repository**
   - Push code to GitHub
   - Import project in Vercel

2. **Configure Environment**
   - Set `NEXT_PUBLIC_API_URL` to Railway backend URL

3. **Deploy**
   - Vercel automatically deploys on push

#### Backend Deployment (Railway)

1. **Create Railway Account**
   - Sign up at railway.app

2. **Create New Project**
   - Add PostgreSQL service
   - Add Redis service
   - Add Python service for FastAPI

3. **Configure Environment Variables**
```
DATABASE_URL=<Railway PostgreSQL URL>
REDIS_URL=<Railway Redis URL>
SECRET_KEY=<generate-secure-key>
ENVIRONMENT=production
DEBUG=False
```

4. **Deploy**
   - Connect GitHub repository
   - Railway auto-deploys on push

---

### Option 3: Heroku

#### Steps

1. **Install Heroku CLI**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create App**
```bash
heroku create finnova-ai
```

4. **Add PostgreSQL and Redis**
```bash
heroku addons:create heroku-postgresql:standard-0 -a finnova-ai
heroku addons:create heroku-redis:premium-0 -a finnova-ai
```

5. **Configure Environment**
```bash
heroku config:set SECRET_KEY=<generate-key> -a finnova-ai
heroku config:set ENVIRONMENT=production -a finnova-ai
```

6. **Deploy**
```bash
git push heroku main
```

---

### Option 4: AWS ECS + RDS

#### Architecture
- ECS Fargate for containerized app
- RDS PostgreSQL for database
- ElastiCache for Redis
- S3 for file uploads
- CloudFront for static content

#### Steps

1. **Build Docker Image**
```bash
docker build -t finnova-ai:latest .
docker tag finnova-ai:latest <account>.dkr.ecr.<region>.amazonaws.com/finnova-ai:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/finnova-ai:latest
```

2. **Create RDS Instance**
   - PostgreSQL 15
   - Multi-AZ enabled
   - Automatic backups

3. **Create ElastiCache**
   - Redis 7
   - Multi-AZ enabled

4. **Create ECS Cluster**
   - Fargate launch type
   - 2 vCPU, 4GB memory

5. **Create Task Definition**
   - Image: ECR repository
   - Environment variables from Secrets Manager

6. **Create Service**
   - ECS task
   - Load Balancer
   - Auto-scaling

---

## Production Checklist

- [ ] Enable HTTPS
- [ ] Set secure SECRET_KEY
- [ ] Configure CORS properly
- [ ] Set DEBUG=False
- [ ] Enable database backups
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Set up error tracking (Sentry)
- [ ] Enable rate limiting
- [ ] Configure email service
- [ ] Set up CDN
- [ ] Configure domain name
- [ ] Enable API authentication
- [ ] Set up CI/CD pipeline

---

## Scaling

### Horizontal Scaling
- Use load balancer
- Deploy multiple app instances
- Use managed database

### Vertical Scaling
- Increase CPU/Memory per instance
- Upgrade database tier

### Caching
- Redis for session cache
- CloudFront for static assets
- Database query caching

---

## Monitoring

### Tools
- New Relic
- DataDog
- Prometheus + Grafana
- Sentry (error tracking)

### Metrics
- API response time
- Database query performance
- Memory usage
- CPU usage
- Error rate

---

## Backup & Recovery

### Database Backups
- Automated daily backups
- Point-in-time recovery enabled
- Multi-region backups

### File Backups
- S3 versioning enabled
- Cross-region replication

---

## Security

- Enable HTTPS/TLS
- Use environment variables for secrets
- Implement rate limiting
- Enable CORS validation
- Use secure session cookies
- Enable CSRF protection
- Implement input validation
- Regular security audits

---

## Support

For issues during deployment, refer to:
- Docker documentation
- FastAPI deployment guide
- Next.js deployment guide
- Platform-specific documentation

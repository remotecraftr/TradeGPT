# Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- AWS account configured
- Kubernetes cluster available
- GitHub Actions secrets configured

## Local Development Deployment

```bash
# Setup environment
cp .env.example .env

# Build and run containers
docker-compose up -d

# Run migrations
docker-compose exec app python manage.py migrate

# Create superuser
docker-compose exec app python manage.py createsuperuser

# Access application
open http://localhost:8000
```

## Docker Deployment

```bash
# Build image
docker build -t remote-crafter:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  remote-crafter:latest

# Push to registry
docker tag remote-crafter:latest yourusername/remote-crafter:latest
docker push yourusername/remote-crafter:latest
```

## AWS ECS Deployment

```bash
# Create ECR repository
aws ecr create-repository --repository-name remote-crafter

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t remote-crafter:latest .
docker tag remote-crafter:latest <account>.dkr.ecr.us-east-1.amazonaws.com/remote-crafter:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/remote-crafter:latest
```

## Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace remote-crafter

# Apply configurations
kubectl apply -f k8s/configmap.yaml -n remote-crafter
kubectl apply -f k8s/secrets.yaml -n remote-crafter
kubectl apply -f k8s/deployment.yaml -n remote-crafter
kubectl apply -f k8s/service.yaml -n remote-crafter

# Check deployment
kubectl get pods -n remote-crafter

# View logs
kubectl logs -f deployment/remote-crafter -n remote-crafter
```

## Database Migrations

```bash
# Create migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

## Monitoring & Logging

```bash
# View application logs
docker-compose logs -f app

# Monitor Kubernetes pods
kubectl top pods -n remote-crafter

# Access metrics
open http://grafana.example.com
```

## Rollback Procedures

```bash
# Docker rollback
docker run -p 8000:8000 remote-crafter:previous-tag

# Kubernetes rollback
kubectl rollout undo deployment/remote-crafter -n remote-crafter

# Check rollout history
kubectl rollout history deployment/remote-crafter -n remote-crafter
```

## Health Checks

```bash
# Application health
curl http://localhost:8000/health

# Database health
psql -U user -d remote_crafter -c "SELECT 1"

# Cache health
redis-cli ping
```

## Backup & Recovery

```bash
# Backup database
pg_dump -U user remote_crafter > backup.sql

# Restore database
psql -U user remote_crafter < backup.sql

# Backup volume
docker run --rm -v db_data:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/db_backup.tar.gz -C /data .
```

## Troubleshooting

Common deployment issues and solutions:

1. **Connection refused**: Check network configuration and firewall rules
2. **Out of memory**: Increase container memory limits
3. **Database lock**: Check active connections and queries
4. **Cache issues**: Clear Redis and restart cache service

## Production Checklist

- [ ] Set environment to production
- [ ] Configure SSL certificates
- [ ] Setup database backups
- [ ] Configure monitoring and alerting
- [ ] Setup log aggregation
- [ ] Test disaster recovery procedures
- [ ] Document runbooks
- [ ] Configure load balancing
- [ ] Setup CDN for static assets
- [ ] Enable rate limiting

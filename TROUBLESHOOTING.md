# Troubleshooting Guide

## Common Issues and Solutions

### Application Issues

#### Issue: Application Won't Start
```
Error: Address already in use
```

**Solution:**
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python manage.py runserver 8001
```

#### Issue: Database Connection Failed
```
Error: could not connect to server
```

**Solution:**
```bash
# Check database status
psql -U user -h localhost -c "SELECT 1"

# Check environment variables
echo $DATABASE_URL

# Verify credentials
psql -U user -h localhost -d remote_crafter -c "SELECT 1"
```

### Docker Issues

#### Issue: Container Won't Start
```
Error: docker: Error response from daemon
```

**Solution:**
```bash
# Check Docker daemon
docker ps

# View container logs
docker logs container_name

# Rebuild image
docker build --no-cache -t remote-crafter:latest .

# Remove dangling images
docker image prune -a
```

#### Issue: Out of Disk Space
```
Error: No space left on device
```

**Solution:**
```bash
# Check disk usage
df -h

# Clean up Docker
docker system prune -a

# Remove unused volumes
docker volume prune

# Clear logs
docker exec container truncate -s 0 /var/lib/docker/containers/*/*-json.log
```

### Database Issues

#### Issue: Slow Queries
```sql
-- Check slow query log
SHOW slow_query_log;

-- Query execution plan
EXPLAIN ANALYZE SELECT ...
```

**Solution:**
```sql
-- Create missing indexes
CREATE INDEX idx_users_email ON users(email);

-- Analyze table statistics
ANALYZE users;

-- Check query plan
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'test@example.com';
```

#### Issue: Connection Pool Exhausted
```
Error: sorry, too many clients already
```

**Solution:**
```sql
-- Check active connections
SELECT COUNT(*) FROM pg_stat_activity;

-- Check max connections
SHOW max_connections;

-- Increase max connections
ALTER SYSTEM SET max_connections = 300;

-- Or restart PostgreSQL
sudo systemctl restart postgresql
```

### Cache Issues

#### Issue: Cache Not Working
```
Error: Redis connection refused
```

**Solution:**
```bash
# Check Redis status
redis-cli ping

# Start Redis
redis-server

# Check Redis connection
redis-cli -h localhost -p 6379

# Clear cache
redis-cli FLUSHALL
```

### Performance Issues

#### Issue: High CPU Usage
```bash
# Monitor CPU usage
top

# Check for resource-heavy processes
ps aux --sort=-%cpu | head -20

# Profile application
python -m cProfile manage.py runserver
```

#### Issue: High Memory Usage
```bash
# Check memory usage
free -h

# Monitor with top
top -b -u appuser

# Profile memory usage
python -m memory_profiler script.py
```

### API Issues

#### Issue: 500 Internal Server Error
```
Error: Internal Server Error
```

**Solution:**
```bash
# Check application logs
tail -f /var/log/remote-crafter.log

# Check Django debug
DEBUG=True python manage.py runserver

# Check error traceback
# Review application errors in logs
```

#### Issue: CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
```python
# Update CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]

# Or use CORS_ALLOW_ALL_ORIGINS = True for development only
```

#### Issue: Rate Limiting
```
Error: 429 Too Many Requests
```

**Solution:**
```bash
# Check rate limit configuration
# Increase rate limit threshold
# Use cache key instead of IP for authenticated users
```

### Authentication Issues

#### Issue: JWT Token Expired
```
Error: Token is invalid or expired
```

**Solution:**
```bash
# Use refresh token
POST /api/auth/refresh
{
  "refresh_token": "token"
}

# Or login again
POST /api/auth/login
```

#### Issue: Authentication Failed
```
Error: Invalid credentials
```

**Solution:**
```bash
# Check user exists
python manage.py shell
from django.contrib.auth import authenticate
authenticate(username='user', password='pass')

# Reset password
python manage.py changepassword username
```

### Deployment Issues

#### Issue: Health Check Failing
```bash
# Check health endpoint
curl http://localhost:8000/health

# Verify dependencies
# Database connection
# Cache connection
# External services
```

#### Issue: Rolling Update Failed
```bash
# Check deployment status
kubectl get deployment

# View pod logs
kubectl logs pod_name

# Rollback deployment
kubectl rollout undo deployment/remote-crafter
```

## Debugging Tools

### Django Debug Toolbar
```python
# Install
pip install django-debug-toolbar

# Add to settings
INSTALLED_APPS = [
    'debug_toolbar',
]

# Add to urls
if DEBUG:
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
```

### Logging Configuration
```python
# Enable detailed logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
}
```

## Getting Help

- Check logs: `/var/log/remote-crafter.log`
- Application logs: `docker logs container_name`
- Database logs: `pg_dump -U user`
- System logs: `journalctl -u remote-crafter`
- Documentation: `https://docs.remote-crafter.com`
- Issues: `https://github.com/yourusername/remote-crafter/issues`

## Support

For issues not listed here:
- Create GitHub issue with error logs
- Email support@remote-crafter.com
- Join Discord community for quick help

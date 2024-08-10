# Performance Optimization Guide

## Introduction
This guide provides best practices for optimizing performance across the Remote Crafter platform.

## Database Optimization

### Query Optimization
```python
# ❌ Bad: N+1 query problem
for user in User.objects.all():
    print(user.profile.bio)

# ✅ Good: Use select_related
users = User.objects.select_related('profile').all()
for user in users:
    print(user.profile.bio)
```

### Indexing Strategy
```sql
-- Create indexes on frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_models_status ON models(status);
```

### Query Monitoring
```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    # Your query here
    pass

print(f"Number of queries: {len(context.captured_queries)}")
for query in context.captured_queries:
    print(query['sql'])
    print(f"Time: {query['time']}s")
```

## Caching Strategies

### Cache Levels
```python
# Level 1: Application Cache (Redis)
from django.core.cache import cache

# Cache result for 1 hour
cache.set('user_projects:' + user_id, projects, 3600)
projects = cache.get('user_projects:' + user_id)

# Level 2: Database Query Cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes
def expensive_api_view(request):
    return Response(data)

# Level 3: HTTP Cache Headers
response['Cache-Control'] = 'public, max-age=3600'
```

### Cache Invalidation
```python
def update_project(project_id, **kwargs):
    # Update project
    project = Project.objects.get(id=project_id)
    for key, value in kwargs.items():
        setattr(project, key, value)
    project.save()
    
    # Invalidate cache
    cache.delete(f'project:{project_id}')
    cache.delete(f'user_projects:{project.user_id}')
```

## API Performance

### Pagination
```python
# Reduce data transfer
GET /api/projects?page=1&limit=20

class ProjectListView(ViewSet):
    pagination_class = PageNumberPagination
    page_size = 20
```

### Response Compression
```python
# gzip compression for all responses
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
]
```

### Field Selection
```python
# Only request needed fields
GET /api/projects?fields=id,name,created_at

class ProjectSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.context.get('fields')
        if fields:
            allowed = set(fields.split(','))
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
```

## Frontend Performance

### Asset Optimization
```html
<!-- Minimize CSS -->
<link rel="stylesheet" href="styles.min.css">

<!-- Defer non-critical JavaScript -->
<script async src="analytics.js"></script>
<script defer src="app.js"></script>

<!-- Lazy load images -->
<img loading="lazy" src="image.jpg">
```

### Code Splitting
```javascript
// Dynamic imports for code splitting
import('./heavy-module').then(module => {
    // Use module
});
```

## ML Model Performance

### Inference Optimization
```python
# Batch processing for better GPU utilization
def batch_predict(model, inputs, batch_size=32):
    predictions = []
    for i in range(0, len(inputs), batch_size):
        batch = inputs[i:i+batch_size]
        batch_pred = model.predict(batch)
        predictions.extend(batch_pred)
    return predictions
```

### Model Quantization
```python
import torch

# Quantize model for faster inference
quantized_model = torch.quantization.quantize_dynamic(
    original_model,
    {torch.nn.Linear},
    dtype=torch.qint8
)
```

## Monitoring & Profiling

### Application Monitoring
```python
from django_prometheus.exports import ExportToDjangoView

# Track key metrics
from prometheus_client import Counter, Histogram

request_count = Counter('app_requests_total', 'Total requests')
request_duration = Histogram('app_request_duration_seconds', 'Request duration')
```

### Profiling
```python
from django.middleware.common import CommonMiddleware
import cProfile
import pstats

# Profile slow requests
profiler = cProfile.Profile()
profiler.enable()
# Your code here
profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

## Performance Benchmarks

### Current Metrics
- API Response Time: <100ms (p95)
- Database Query Time: <50ms (p95)
- Page Load Time: <2s (p95)
- Cache Hit Rate: >80%
- API Throughput: 1000+ req/s

### Targets
- API Response Time: <50ms (p95)
- Database Query Time: <25ms (p95)
- Cache Hit Rate: >90%
- API Throughput: 5000+ req/s

## Best Practices Checklist

- [ ] Use database indexes on frequently queried columns
- [ ] Implement caching for expensive operations
- [ ] Optimize database queries (select_related, prefetch_related)
- [ ] Use pagination for list endpoints
- [ ] Compress API responses
- [ ] Lazy load non-critical resources
- [ ] Batch process large operations
- [ ] Monitor application performance
- [ ] Profile slow operations
- [ ] Set appropriate cache TTLs

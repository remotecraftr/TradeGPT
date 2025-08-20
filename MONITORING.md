# Monitoring and Observability Guide

## Overview
Comprehensive monitoring strategy for production systems using Prometheus, Grafana, and ELK stack.

## Metrics Collection

### Application Metrics
```python
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
request_count = Counter(
    'app_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'app_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint'],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)

# Database metrics
db_query_count = Counter(
    'db_queries_total',
    'Total database queries',
    ['operation', 'table']
)

db_query_duration = Histogram(
    'db_query_duration_seconds',
    'Database query duration'
)

# Cache metrics
cache_hits = Counter('cache_hits_total', 'Cache hits')
cache_misses = Counter('cache_misses_total', 'Cache misses')

# Model metrics
model_predictions = Counter(
    'model_predictions_total',
    'Total model predictions',
    ['model_id', 'status']
)

model_latency = Histogram(
    'model_prediction_latency_seconds',
    'Model prediction latency'
)
```

## Logging Strategy

### Log Levels
```python
import logging

logger = logging.getLogger(__name__)

# ERROR: System failures and exceptions
logger.error("Database connection failed", exc_info=True)

# WARNING: Potential issues
logger.warning("High memory usage detected")

# INFO: Important events
logger.info("User registered: user_id=123")

# DEBUG: Detailed diagnostic information
logger.debug("SQL query executed: %s", query)
```

### Structured Logging
```python
import json
from pythonjsonlogger import jsonlogger

# JSON logging for easy parsing
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Example log output
logger.info("User action", extra={
    'user_id': '123',
    'action': 'login',
    'timestamp': '2025-05-15T10:30:00Z',
    'duration_ms': 150
})
```

## Alerting Rules

### Critical Alerts
```yaml
groups:
  - name: critical_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(app_requests_total{status="5xx"}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
      
      - alert: DatabaseDown
        expr: up{job="database"} == 0
        for: 1m
        annotations:
          summary: "Database is down"
```

### Warning Alerts
```yaml
groups:
  - name: warning_alerts
    interval: 1m
    rules:
      - alert: HighCacheEviction
        expr: rate(cache_evictions_total[5m]) > 100
        for: 5m
        annotations:
          summary: "High cache eviction rate"
      
      - alert: SlowQueries
        expr: histogram_quantile(0.95, db_query_duration_seconds) > 1
        for: 10m
        annotations:
          summary: "Slow database queries detected"
```

## Dashboards

### Key Performance Indicators
- API Response Time (p50, p95, p99)
- Error Rate (4xx, 5xx)
- Request Throughput (req/s)
- Database Query Time
- Cache Hit Rate
- Model Prediction Latency

### Resource Utilization
- CPU Usage
- Memory Usage
- Disk Usage
- Network I/O
- Database Connections

## Health Checks

### Application Health
```python
from django.http import JsonResponse

def health_check(request):
    checks = {
        'database': check_database(),
        'cache': check_cache(),
        'models': check_models(),
        'disk_space': check_disk_space()
    }
    
    status = 'healthy' if all(checks.values()) else 'unhealthy'
    return JsonResponse({
        'status': status,
        'checks': checks,
        'timestamp': timezone.now()
    })

def check_database():
    try:
        connection.ensure_connection()
        return True
    except:
        return False

def check_cache():
    try:
        cache.set('health_check', 'ok', 60)
        return cache.get('health_check') == 'ok'
    except:
        return False
```

## Tracing

### Distributed Tracing
```python
from opentelemetry import trace, metrics
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

# Trace a request
@app.route('/api/predict')
def predict():
    with tracer.start_as_current_span("predict_request") as span:
        span.set_attribute("model_id", model_id)
        
        # Your code here
        result = model.predict(data)
        
        span.set_attribute("status", "success")
        return result
```

## Log Aggregation (ELK)

### Elasticsearch Indexing
```
remote-crafter-app-YYYY.MM.DD
remote-crafter-db-YYYY.MM.DD
remote-crafter-errors-YYYY.MM.DD
```

### Kibana Queries
```
# Errors in last 24 hours
level: ERROR AND @timestamp: [now-24h TO now]

# Slow API requests
method: POST AND request_duration_ms: [>1000 TO *]

# Failed authentication attempts
event: login_failed AND @timestamp: [now-1h TO now]
```

## SLA Monitoring

### Key Metrics
- API Availability: 99.99%
- API Response Time: <100ms (p95)
- Database Uptime: 99.99%
- Cache Hit Rate: >85%

### Reporting
- Daily status report
- Weekly performance analysis
- Monthly SLA review
- Quarterly trend analysis

## Best Practices

- Monitor at multiple levels (application, infrastructure, business)
- Set appropriate alert thresholds
- Regular alert tuning and adjustment
- Automated runbook generation
- Continuous monitoring of monitoring systems
- Regular alerting drills
- Post-incident analysis and improvements

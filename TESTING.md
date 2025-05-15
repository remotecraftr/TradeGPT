# Testing Strategy and Guidelines

## Test Structure

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_serializers.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   ├── test_database.py
│   └── test_workflows.py
├── e2e/
│   ├── test_user_flows.py
│   └── test_api_flows.py
├── performance/
│   └── test_benchmarks.py
└── conftest.py
```

## Unit Tests

### Database Models
```python
import pytest
from django.test import TestCase
from myapp.models import User, Project

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
    
    def test_user_creation(self):
        assert self.user.email == 'test@example.com'
        assert self.user.is_active == True
    
    def test_user_string_representation(self):
        assert str(self.user) == 'test@example.com'
```

### Serializers
```python
from rest_framework.test import APITestCase
from myapp.serializers import UserSerializer

class UserSerializerTest(APITestCase):
    def test_serializer_with_valid_data(self):
        data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()
    
    def test_serializer_with_invalid_data(self):
        data = {'email': 'invalid-email'}
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
```

## Integration Tests

### API Endpoints
```python
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

class UserAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_registration(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post('/api/auth/register', data)
        assert response.status_code == 201
        assert User.objects.filter(email='newuser@example.com').exists()
    
    def test_user_login(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login', data)
        assert response.status_code == 200
        assert 'access_token' in response.data
```

## End-to-End Tests

```python
from django.test import TestCase, Client

class UserFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_complete_user_workflow(self):
        # Register
        response = self.client.post('/register', {
            'email': 'user@example.com',
            'password': 'pass123'
        })
        assert response.status_code == 200
        
        # Login
        response = self.client.post('/login', {
            'email': 'user@example.com',
            'password': 'pass123'
        })
        assert response.status_code == 200
        
        # Create project
        response = self.client.post('/projects', {
            'name': 'Test Project'
        })
        assert response.status_code == 201
```

## Performance Tests

```python
import pytest
from django.test import TestCase
from django.test.utils import override_settings

@override_settings(DEBUG=True)
class PerformanceTest(TestCase):
    @pytest.mark.slow
    def test_api_response_time(self):
        start = time.time()
        response = self.client.get('/api/projects')
        end = time.time()
        
        assert response.status_code == 200
        assert (end - start) < 0.1  # Less than 100ms
    
    def test_database_query_count(self):
        with self.assertNumQueries(5):
            Project.objects.select_related('user').all()
```

## Running Tests

### All Tests
```bash
pytest
pytest --cov=. --cov-report=html
```

### Specific Tests
```bash
pytest tests/unit/
pytest tests/integration/test_api.py::UserAPITest::test_user_login
pytest -k "test_user" -v
pytest -m "not slow"
```

### With Coverage
```bash
pytest --cov=. --cov-report=term-missing --cov-fail-under=80
```

## Test Fixtures

```python
@pytest.fixture
def user(db):
    return User.objects.create(
        email='test@example.com',
        first_name='Test'
    )

@pytest.fixture
def project(db, user):
    return Project.objects.create(
        name='Test Project',
        user=user
    )

def test_project_creation(project):
    assert project.name == 'Test Project'
    assert project.user.email == 'test@example.com'
```

## Mocking

```python
from unittest.mock import patch, MagicMock

@patch('myapp.services.external_api.call')
def test_with_mock(mock_api):
    mock_api.return_value = {'status': 'success'}
    result = my_function()
    assert result == {'status': 'success'}
    mock_api.assert_called_once()
```

## CI/CD Integration

Tests run automatically on:
- Every push to main/develop
- Every pull request
- Nightly scheduled runs
- Before production deployment

## Coverage Goals

- **Unit Tests**: >90% coverage
- **Integration Tests**: >80% coverage
- **Total**: >85% coverage
- **Critical Paths**: 100% coverage

## Best Practices

- Write tests before code (TDD)
- Test edge cases and error scenarios
- Keep tests independent and isolated
- Use meaningful test names
- Mock external dependencies
- Maintain test data consistency
- Regular test review and maintenance

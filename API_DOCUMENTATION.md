# API Documentation

## Base URL
```
https://api.remote-crafter.com/v1
```

## Authentication

All API requests require authentication using JWT tokens.

### Obtain Token
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

### Use Token
```bash
Authorization: Bearer {access_token}
```

## Endpoints

### User Management

#### Register User
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}

Response: 201 Created
{
  "id": "uuid",
  "email": "newuser@example.com",
  "first_name": "John",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get User Profile
```bash
GET /users/profile
Authorization: Bearer {token}

Response: 200 OK
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Projects

#### List Projects
```bash
GET /projects?page=1&limit=20&sort=-created_at
Authorization: Bearer {token}

Response: 200 OK
{
  "data": [
    {
      "id": "uuid",
      "name": "Project Name",
      "description": "Project description",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

#### Create Project
```bash
POST /projects
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "New Project",
  "description": "Project description",
  "team_id": "uuid"
}

Response: 201 Created
{
  "id": "uuid",
  "name": "New Project",
  "description": "Project description",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### ML Models

#### Get Model Details
```bash
GET /models/{model_id}
Authorization: Bearer {token}

Response: 200 OK
{
  "id": "uuid",
  "name": "Model Name",
  "version": "1.0.0",
  "status": "ready",
  "accuracy": 0.95,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Train Model
```bash
POST /models/{model_id}/train
Authorization: Bearer {token}
Content-Type: application/json

{
  "dataset_id": "uuid",
  "hyperparameters": {
    "learning_rate": 0.001,
    "epochs": 100
  }
}

Response: 202 Accepted
{
  "job_id": "uuid",
  "status": "queued"
}
```

#### Make Prediction
```bash
POST /models/{model_id}/predict
Authorization: Bearer {token}
Content-Type: application/json

{
  "input": {
    "feature1": 1.5,
    "feature2": "value",
    "feature3": [1, 2, 3]
  }
}

Response: 200 OK
{
  "prediction": "class_a",
  "confidence": 0.98,
  "processing_time_ms": 125
}
```

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "email": "Invalid email format"
    }
  }
}
```

### Common Error Codes
- `AUTH_ERROR`: Authentication failed (401)
- `VALIDATION_ERROR`: Invalid request data (400)
- `NOT_FOUND`: Resource not found (404)
- `PERMISSION_DENIED`: Access denied (403)
- `INTERNAL_ERROR`: Server error (500)

## Rate Limiting

- 1000 requests per hour per API key
- Headers returned:
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Unix timestamp of limit reset

## Webhooks

Subscribe to events for real-time updates:

```bash
POST /webhooks
Authorization: Bearer {token}
Content-Type: application/json

{
  "url": "https://yourapp.com/webhooks",
  "events": ["model.trained", "job.completed"],
  "secret": "your-secret-key"
}
```

## SDKs

- Python: `pip install remote-crafter`
- JavaScript: `npm install @remote-crafter/sdk`
- Go: `go get github.com/remote-crafter/sdk-go`

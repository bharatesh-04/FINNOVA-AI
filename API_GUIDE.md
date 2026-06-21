# API Integration Guide

## Authentication

All API endpoints require JWT authentication (except `/auth/register` and `/auth/login`).

### Getting Started

1. **Register**
```bash
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user"
  }
}
```

2. **Store tokens securely**
   - Access token: Store in memory (valid for 30 minutes)
   - Refresh token: Store in secure cookie (valid for 7 days)

3. **Make authenticated requests**
```bash
GET /api/v1/transactions
Authorization: Bearer <access_token>
```

### Refreshing Token

```bash
POST /api/v1/auth/refresh
{
  "token": "<refresh_token>"
}
```

---

## Common Use Cases

### 1. Add an Expense

```bash
POST /api/v1/transactions
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "type": "expense",
  "amount": 250.50,
  "currency": "INR",
  "category": "food",
  "merchant": "Starbucks",
  "description": "Coffee and breakfast",
  "date": "2024-01-15T10:30:00Z",
  "tags": ["breakfast", "cafe"],
  "notes": "Meeting with John"
}
```

### 2. Get Financial Dashboard Stats

```bash
GET /api/v1/transactions/dashboard-stats
Authorization: Bearer <access_token>
```

Response:
```json
{
  "total_balance": 45000,
  "total_income": 100000,
  "total_expenses": 55000,
  "total_savings": 45000,
  "net_worth": 45000,
  "financial_health_score": 75
}
```

### 3. Get Spending Trends

```bash
GET /api/v1/analytics/spending-trends?period=monthly
Authorization: Bearer <access_token>
```

### 4. Create a Budget

```bash
POST /api/v1/budgets
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Monthly Food Budget",
  "budget_type": "category",
  "amount": 5000,
  "currency": "INR",
  "category": "food",
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-01-31T23:59:59Z"
}
```

### 5. Create a Savings Goal

```bash
POST /api/v1/goals
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Vacation Fund",
  "target_amount": 50000,
  "currency": "INR",
  "deadline": "2024-12-31T00:00:00Z",
  "category": "travel",
  "priority": "high"
}
```

### 6. Upload Receipt

```bash
POST /api/v1/receipts/upload
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

[Upload file as multipart form]
```

### 7. Chat with AI Assistant

```bash
POST /api/v1/chat/message
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "content": "How much did I spend on food this month?"
}
```

Response:
```json
{
  "role": "assistant",
  "content": "Based on your transactions, you spent ₹3,200 on food this month...",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Invalid credentials"
}
```

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 404 Not Found
```json
{
  "detail": "Transaction not found"
}
```

### 500 Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

- 100 requests per minute per user (default)
- Endpoints with upload: 10 requests per minute

---

## Pagination

Most list endpoints support pagination:

```bash
GET /api/v1/transactions?limit=10&offset=0
```

Response includes:
- `items`: Array of results
- `total`: Total count
- `limit`: Items per page
- `offset`: Current offset

---

## Filtering

### Transactions
```bash
GET /api/v1/transactions?start_date=2024-01-01&end_date=2024-01-31&category=food&type=expense
```

### Budgets
```bash
GET /api/v1/budgets?status=active
```

### Goals
```bash
GET /api/v1/goals?status=active
```

---

## Webhook Events

Real-time events available via WebSocket:
- Budget exceeded
- Fraud alert
- Goal reached
- New insight generated

```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Handle event
};
```

---

## Best Practices

1. **Always validate user input**
   - Check required fields
   - Validate data types
   - Sanitize strings

2. **Handle errors gracefully**
   - Implement retry logic
   - Show user-friendly error messages
   - Log errors for debugging

3. **Implement caching**
   - Cache dashboard stats
   - Cache category list
   - Invalidate on data change

4. **Optimize API calls**
   - Batch requests when possible
   - Use pagination for large lists
   - Implement request debouncing

5. **Security**
   - Never expose access token in URL
   - Use HTTPS only
   - Implement CSRF protection
   - Validate CORS origins

---

## Sandbox Environment

Test your integration against:
- URL: https://sandbox-api.finnovaai.com
- Test credentials available in documentation

---

## SDK Libraries

Official SDKs available for:
- JavaScript/TypeScript
- Python
- Java
- Go

---

## Need Help?

- API Documentation: `/docs`
- GitHub Issues: github.com/finnovaai/finnova-ai
- Email: api-support@finnovaai.com

# API Documentation

## Base URL
`http://localhost:8000`

## Authentication
All endpoints require Basic Authentication.

**Credentials:** `admin` / `secure123`

**Header:** `Authorization: Basic YWRtaW46c2VjdXJlMTIz`

---

## Endpoints

### 1. GET /transactions

List all transactions.

**Request:**
```bash
curl -X GET http://localhost:8000/transactions -u admin:secure123
```

**Response (200):**
```json
{
  "count": 2,
  "transactions": [
    {
      "id": "1",
      "type": "SEND",
      "amount": 5000,
      "sender": "0791234567",
      "receiver": "0797654321",
      "timestamp": "2024-01-15T10:30:00",
      "status": "completed",
      "reference": "TXN000001"
    }
  ]
}
```

---

### 2. GET /transactions/{id}

Get single transaction.

**Request:**
```bash
curl -X GET http://localhost:8000/transactions/1 -u admin:secure123
```

**Response (200):**
```json
{
  "transaction": {
    "id": "1",
    "type": "SEND",
    "amount": 5000,
    "sender": "0791234567",
    "receiver": "0797654321",
    "timestamp": "2024-01-15T10:30:00",
    "status": "completed",
    "reference": "TXN000001"
  }
}
```

**Error (404):**
```json
{
  "error": "Transaction 999 not found"
}
```

---

### 3. POST /transactions

Create new transaction.

**Request:**
```bash
curl -X POST http://localhost:8000/transactions \
  -u admin:secure123 \
  -H "Content-Type: application/json" \
  -d '{
    "type": "SEND",
    "amount": 1500,
    "sender": "0791234567",
    "receiver": "0798888888"
  }'
```

**Required Fields:**
- `type`: SEND, RECEIVE, DEPOSIT, WITHDRAW, PAYMENT
- `amount`: Number > 0
- `sender`: String
- `receiver`: String

**Response (201):**
```json
{
  "message": "Transaction created",
  "transaction": {
    "id": "26",
    "type": "SEND",
    "amount": 1500,
    "sender": "0791234567",
    "receiver": "0798888888",
    "timestamp": "2024-01-22T15:30:00",
    "status": "completed",
    "reference": "TXN000026"
  }
}
```

**Error (400):**
```json
{
  "error": "Missing fields: type, amount"
}
```

---

### 4. PUT /transactions/{id}

Update transaction.

**Request:**
```bash
curl -X PUT http://localhost:8000/transactions/1 \
  -u admin:secure123 \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 6000,
    "status": "completed"
  }'
```

**Response (200):**
```json
{
  "message": "Transaction updated",
  "transaction": {
    "id": "1",
    "type": "SEND",
    "amount": 6000,
    "sender": "0791234567",
    "receiver": "0797654321",
    "timestamp": "2024-01-15T10:30:00",
    "status": "completed",
    "reference": "TXN000001"
  }
}
```

**Error (404):**
```json
{
  "error": "Transaction 999 not found"
}
```

---

### 5. DELETE /transactions/{id}

Delete transaction.

**Request:**
```bash
curl -X DELETE http://localhost:8000/transactions/1 -u admin:secure123
```

**Response (200):**
```json
{
  "message": "Transaction deleted",
  "transaction": {
    "id": "1",
    "type": "SEND",
    "amount": 5000,
    "sender": "0791234567",
    "receiver": "0797654321",
    "timestamp": "2024-01-15T10:30:00",
    "status": "completed",
    "reference": "TXN000001"
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Server Error |

---

## Security

### Basic Authentication Limitations

**Weaknesses:**
1. Credentials transmitted in base64 (not encrypted)
2. Sent with every request
3. No expiration
4. Vulnerable to interception without HTTPS

**Recommended Alternatives:**

**JWT (JSON Web Tokens):**
- Tokens expire automatically
- Stateless authentication
- Industry standard

**OAuth 2.0:**
- Delegated authorization
- Refresh tokens
- Third-party integration

**Best Practice:** Always use HTTPS in production.

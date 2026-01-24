# REST API - MoMo SMS Transactions

Author: Binthia Nitonde
REST API for MoMo SMS transaction data using Python's `http.server` module.

## Endpoints

- `GET /transactions` - Retrieve all transactions
- `POST /transactions` - Create new transaction

## Setup

```bash
# Create folders
mkdir -p dsa enshots

# Generate sample data
python3 scripts/create_sample_data.py

# Start server
python3 api/rest_server.py
```

Server runs on `http://localhost:8000`

## Authentication

- Username: `admin`
- Password: `secure123`

## API Usage

### GET /transactions

```bash
curl -X GET http://localhost:8000/transactions -u admin:secure123
```

### POST /transactions

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
- `type` - SEND, RECEIVE, DEPOSIT, WITHDRAW, PAYMENT
- `amount` - Number > 0
- `sender` - Non-empty string
- `receiver` - Non-empty string

## Testing

### Required Screenshots

1. `screenshots/get_success.png` - GET request (200 OK)
2. `screenshots/post_success.png` - POST request (201 Created)
3. `screenshots/unauthorized.png` - Wrong credentials (401)

### DSA Analysis

```bash
python3 dsa/search_comparison.py
```

Results saved to `dsa/results.txt`

## Error Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Server Error

## Project Structure
```
├── api/
│   ├── rest_server.py              # REST API server
│   └── collection_handlers.py      # Business logic
├── dsa/
│   ├── search_comparison.py        # Performance analysis
│   └── results.txt                 # Results
├── screenshots/
│   ├── get_success.png
│   ├── post_success.png
│   └── unauthorized.png

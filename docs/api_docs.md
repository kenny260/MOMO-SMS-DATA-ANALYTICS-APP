# API Documentation – Authentication & Delete Endpoint

**Author:** Cédric Bigwi Hindura  
**Responsibility:** API Security & DELETE Endpoint

---

## Authentication (Basic Auth)

All API endpoints are protected using **HTTP Basic Authentication**.

Each request must include this header:

Authorization: Basic base64(username:password)


If the header is missing or invalid, the server returns:

401 Unauthorized


Authentication is checked before any endpoint logic is executed.

---

## DELETE /transactions/{id}

### Description
Deletes a transaction using its ID.

### Endpoint
DELETE /transactions/{id}


### Example
```bash
curl -X DELETE http://localhost:8000/transactions/3 -u admin:password123
Responses
Code	Meaning
200	Deleted successfully
401	Unauthorized
404	Transaction not found
Error Handling
Invalid or missing credentials → 401 Unauthorized

Non-existing transaction ID → 404 Not Found

Implementation Files
api/
 ├── auth.py
 └── handlers_delete.py

# MOMO-SMS-DATA-ANALYTICS-APP

## Team Participation Sheet

This document tracks individual contributions, tasks, and weekly participation of each team member:

🔗 **Google Sheet:**  
https://docs.google.com/spreadsheets/d/1KIyzzSOkjVcdM_NyRWG-wIBQg5_ztDkq1DnAGGdp6ig/edit?usp=sharing


## Project Description
A fullstack pipeline to parse MoMo SMS XML, clean and categorize transactions, store them in SQLite, and visualize analytics via a lightweight dashboard.

# Team Name: MoMo SMS Analytics Team

## Team Members
- Binthia Nitonde - GitHub Repository Setup & Backend Development
- Cedric Bigwi Hindura- System Architecture & Database Design  
- Cherish Yusuf - Scrum Master & Frontend Development

## Architecture
![Architecture Diagram](docs/architecture.png)

## Scrum Board
https://trello.com/invite/b/696362d52dfc3aa699034cce/ATTIe44c47408f5b74f9708de37808690e43B1EE2C98/group-9-momo-sms-data-dashboard-scrum-board

NOTE- We used TRELLO for our scrum board; to view the board, please log in with a free Trello account.

## Database Design & Implementation

The database layer was designed to support efficient storage, querying, and analysis of MoMo SMS transaction data. A normalized relational schema was derived from the MoMo SMS XML structure, covering Users, Transactions, Transaction Categories, and System Logs, with enforced data integrity, security constraints, and performance indexing.

📄 **Full database documentation is available in:**  
![design_rationale.md](docs/design_rationale.md)

## Project Structure
```
├── web/              # Frontend dashboard
├── data/             # Data storage and logs
├── etl/              # ETL pipeline modules
├── api/              # API endpoints (optional)
├── scripts/          # Utility scripts
├── tests/            # Unit tests
└── docs/             # Documentation
```

## Setup
```bash
# Clone repository
git clone https://github.com/kenny260/MOMO-SMS-DATA-ANALYTICS-APP.git

# Install dependencies
pip install -r requirements.txt
```

### Parse Data
```bash
python3 dsa/xml_parser.py
```

### Start Server
```bash
python3 api/server.py
```

Server runs on `http://localhost:8000`

## Authentication

**Credentials:** `admin` / `secure123`

```bash
curl -u admin:secure123 http://localhost:8000/transactions
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/transactions` | List all |
| GET | `/transactions/{id}` | Get one |
| POST | `/transactions` | Create |
| PUT | `/transactions/{id}` | Update |
| DELETE | `/transactions/{id}` | Delete |

## Quick Test

```bash
# List all
curl -X GET http://localhost:8000/transactions -u admin:secure123

# Get one
curl -X GET http://localhost:8000/transactions/1 -u admin:secure123

# Create
curl -X POST http://localhost:8000/transactions \
  -u admin:secure123 \
  -H "Content-Type: application/json" \
  -d '{"type":"SEND","amount":1000,"sender":"A","receiver":"B"}'

# Update
curl -X PUT http://localhost:8000/transactions/1 \
  -u admin:secure123 \
  -H "Content-Type: application/json" \
  -d '{"amount":2000}'

# Delete
curl -X DELETE http://localhost:8000/transactions/1 -u admin:secure123
```

## DSA Analysis

```bash
python3 dsa/search_compare.py
```

Results saved to `dsa/results.txt`

## Project Structure

```
├── api/
│   └── server.py
├── dsa/
│   ├── xml_parser.py
│   └── search_compare.py
├── docs/
│   └── api_docs.md
├── screenshots/
├── data/
│   └── transactions.json
├── modified_sms_v2.xml
└── README.md
```

## Documentation

See `docs/api_docs.md` for complete API documentation.


## Technologies Used
- Python, SQLite, HTML/CSS/JavaScript
- ETL: lxml, dateutil
- API: FastAPI

---
*Week 1 - Team Setup and Planning*

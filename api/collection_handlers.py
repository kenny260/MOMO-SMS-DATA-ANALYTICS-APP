#!/usr/bin/env python3
"""
Transaction Collection Handler

Implements business logic for:
- GET /transactions
- POST /transactions

Integrates with existing ETL pipeline and JSON-based storage.
"""

import json
import os
import sys
from datetime import datetime

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TransactionCollectionHandler:
    """
    Handles transaction collection operations:
    listing all transactions and creating new transactions.
    """

    def __init__(self):
        """Initialize handler and load existing data"""
        self.processed_data = "data/processed/dashboard.json"
        self.backup_data = "data/transactions.json"

        self.transactions = []
        self.next_id = 1
        self._load_data()

    def _load_data(self):
        """Load transactions from ETL output or backup storage"""

        if os.path.exists(self.processed_data):
            try:
                with open(self.processed_data, "r") as f:
                    data = json.load(f)

                    if isinstance(data, dict) and "transactions" in data:
                        self.transactions = data["transactions"]
                    elif isinstance(data, list):
                        self.transactions = data
                    else:
                        self.transactions = []

            except Exception:
                self.transactions = []

        elif os.path.exists(self.backup_data):
            try:
                with open(self.backup_data, "r") as f:
                    self.transactions = json.load(f)
            except Exception:
                self.transactions = []

        else:
            self.transactions = []

        if self.transactions:
            try:
                self.next_id = max(
                    int(t.get("id", 0)) for t in self.transactions
                ) + 1
            except Exception:
                self.next_id = len(self.transactions) + 1

    def _save_data(self):
        """Persist transactions to backup JSON file"""
        try:
            os.makedirs(os.path.dirname(self.backup_data), exist_ok=True)
            with open(self.backup_data, "w") as f:
                json.dump(self.transactions, f, indent=2)
        except Exception:
            pass

    def get_all_transactions(self):
        """
        Retrieve all transactions.

        Returns:
            dict: count and list of transactions
        """
        return {
            "count": len(self.transactions),
            "transactions": self.transactions
        }

    def add_transaction(self, data):
        """
        Create a new transaction with validation.

        Args:
            data (dict): Request payload

        Returns:
            dict: success response or error message
        """

        required_fields = ["type", "amount", "sender", "receiver"]
        missing = [f for f in required_fields if f not in data]

        if missing:
            return {
                "error": f"Missing required fields: {', '.join(missing)}"
            }

        valid_types = ["SEND", "RECEIVE", "DEPOSIT", "WITHDRAW", "PAYMENT"]
        transaction_type = str(data["type"]).upper()

        if transaction_type not in valid_types:
            return {
                "error": f"Invalid transaction type. Must be one of: {', '.join(valid_types)}"
            }

        try:
            amount = float(data["amount"])
            if amount <= 0:
                return {"error": "Amount must be greater than 0"}
        except (ValueError, TypeError):
            return {"error": "Invalid amount format"}

        if not str(data["sender"]).strip():
            return {"error": "Sender cannot be empty"}

        if not str(data["receiver"]).strip():
            return {"error": "Receiver cannot be empty"}

        transaction = {
            "id": str(self.next_id),
            "type": transaction_type,
            "amount": amount,
            "sender": str(data["sender"]).strip(),
            "receiver": str(data["receiver"]).strip(),
            "timestamp": data.get("timestamp", datetime.now().isoformat()),
            "status": data.get("status", "completed"),
            "reference": data.get("reference", f"TXN{self.next_id:06d}")
        }

        if "category" in data:
            transaction["category"] = data["category"]

        if "description" in data:
            transaction["description"] = data["description"]

        self.transactions.append(transaction)
        self.next_id += 1
        self._save_data()

        return {
            "message": "Transaction created successfully",
            "transaction": transaction
        }

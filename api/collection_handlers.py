#!/usr/bin/env python3
"""
Transaction Collection Handler
Business logic for GET /transactions and POST /transactions
"""

import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TransactionCollectionHandler:
    """Handles transaction collection operations"""
    
    def __init__(self):
        """Initialize handler with data sources"""
        self.etl_output = 'data/processed/dashboard.json'
        self.backup_storage = 'data/transactions.json'
        
        self.transactions = []
        self.next_id = 1
        self._load_data()
    
    def _load_data(self):
        """Load transactions from existing data sources"""
        if os.path.exists(self.etl_output):
            try:
                with open(self.etl_output, 'r') as f:
                    data = json.load(f)
                    
                    if isinstance(data, dict) and 'transactions' in data:
                        self.transactions = data['transactions']
                    elif isinstance(data, list):
                        self.transactions = data
                    else:
                        self.transactions = []
                    
                    print(f"Loaded {len(self.transactions)} transactions from ETL output")
                    
            except Exception as e:
                print(f"Warning: Could not load ETL data: {e}")
                self.transactions = []
        
        elif os.path.exists(self.backup_storage):
            try:
                with open(self.backup_storage, 'r') as f:
                    self.transactions = json.load(f)
                print(f"Loaded {len(self.transactions)} transactions from backup")
                
            except Exception as e:
                print(f"Warning: Could not load backup data: {e}")
                self.transactions = []
        
        else:
            print("No existing data found. Starting with empty collection.")
            self.transactions = []
        
        if self.transactions:
            try:
                existing_ids = [int(t.get('id', 0)) for t in self.transactions if 'id' in t]
                if existing_ids:
                    self.next_id = max(existing_ids) + 1
                else:
                    self.next_id = len(self.transactions) + 1
            except:
                self.next_id = len(self.transactions) + 1
    
    def _save_data(self):
        """Save transactions to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.backup_storage), exist_ok=True)
            
            with open(self.backup_storage, 'w') as f:
                json.dump(self.transactions, f, indent=2)
            
            print(f"Saved {len(self.transactions)} transactions")
            
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def get_all_transactions(self):
        """GET /transactions - Returns all transactions"""
        return {
            "count": len(self.transactions),
            "transactions": self.transactions
        }
    
    def add_transaction(self, data):
        """POST /transactions - Creates a new transaction with validation"""
        required_fields = ['type', 'amount', 'sender', 'receiver']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return {
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }
        
        valid_types = ['SEND', 'RECEIVE', 'DEPOSIT', 'WITHDRAW', 'PAYMENT']
        transaction_type = str(data['type']).upper()
        
        if transaction_type not in valid_types:
            return {
                "error": f"Invalid type. Must be one of: {', '.join(valid_types)}"
            }
        
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return {
                    "error": "Amount must be greater than 0"
                }
        except (ValueError, TypeError):
            return {
                "error": "Invalid amount. Must be a number"
            }
        
        if not str(data['sender']).strip():
            return {"error": "Sender cannot be empty"}
        
        if not str(data['receiver']).strip():
            return {"error": "Receiver cannot be empty"}
        
        new_transaction = {
            "id": str(self.next_id),
            "type": transaction_type,
            "amount": amount,
            "sender": str(data['sender']).strip(),
            "receiver": str(data['receiver']).strip(),
            "timestamp": data.get('timestamp', datetime.now().isoformat())
        }
        
        if 'status' in data:
            new_transaction['status'] = data['status']
        
        if 'reference' in data:
            new_transaction['reference'] = data['reference']
        else:
            new_transaction['reference'] = f"TXN{self.next_id:06d}"
        
        if 'category' in data:
            new_transaction['category'] = data['category']
        
        if 'description' in data:
            new_transaction['description'] = data['description']
        
        self.transactions.append(new_transaction)
        self.next_id += 1
        
        self._save_data()
        
        return {
            "message": "Transaction created successfully",
            "transaction": new_transaction
        }

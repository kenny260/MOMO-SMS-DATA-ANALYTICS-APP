#!/usr/bin/env python3
"""
XML Parser for MoMo SMS Transaction Data
Parses modified_sms_v2.xml into JSON format
"""

import xml.etree.ElementTree as ET
import json
import os


def parse_xml_to_json(xml_file='modified_sms_v2.xml', output_file='data/transactions.json'):
    """
    Parse XML SMS records and convert to JSON
    
    Args:
        xml_file: Path to input XML file
        output_file: Path to output JSON file
    
    Returns:
        List of transaction dictionaries
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        transactions = []
        transaction_id = 1
        
        for sms in root.findall('.//sms'):
            transaction = {
                "id": str(transaction_id),
                "type": sms.get('type', 'UNKNOWN').upper(),
                "amount": float(sms.get('amount', 0)),
                "sender": sms.get('sender', ''),
                "receiver": sms.get('receiver', ''),
                "timestamp": sms.get('timestamp', ''),
                "status": sms.get('status', 'completed'),
                "reference": sms.get('reference', f'TXN{transaction_id:06d}')
            }
            
            transactions.append(transaction)
            transaction_id += 1
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(transactions, f, indent=2)
        
        print(f"Parsed {len(transactions)} transactions")
        print(f"Saved to {output_file}")
        
        return transactions
        
    except FileNotFoundError:
        print(f"Error: File '{xml_file}' not found")
        return []
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
        return []


def create_sample_xml(filename='modified_sms_v2.xml'):
    """Create sample XML file with 25+ transactions for testing"""
    
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<sms_records>
    <sms type="SEND" amount="5000" sender="0791234567" receiver="0797654321" 
         timestamp="2024-01-15T10:30:00" status="completed" reference="TXN000001"/>
    <sms type="RECEIVE" amount="3500" sender="0797654321" receiver="0791234567" 
         timestamp="2024-01-15T11:45:00" status="completed" reference="TXN000002"/>
    <sms type="DEPOSIT" amount="10000" sender="0791234567" receiver="BANK" 
         timestamp="2024-01-15T14:20:00" status="completed" reference="TXN000003"/>
    <sms type="WITHDRAW" amount="2000" sender="ATM001" receiver="0791234567" 
         timestamp="2024-01-16T09:15:00" status="completed" reference="TXN000004"/>
    <sms type="PAYMENT" amount="1500" sender="0791234567" receiver="MERCHANT_XYZ" 
         timestamp="2024-01-16T16:30:00" status="completed" reference="TXN000005"/>
    <sms type="SEND" amount="8000" sender="0791234567" receiver="0798888888" 
         timestamp="2024-01-17T08:00:00" status="completed" reference="TXN000006"/>
    <sms type="RECEIVE" amount="4200" sender="0795555555" receiver="0791234567" 
         timestamp="2024-01-17T12:30:00" status="completed" reference="TXN000007"/>
    <sms type="PAYMENT" amount="750" sender="0791234567" receiver="UTILITY_CO" 
         timestamp="2024-01-18T10:00:00" status="completed" reference="TXN000008"/>
    <sms type="SEND" amount="6500" sender="0791234567" receiver="0796666666" 
         timestamp="2024-01-18T15:45:00" status="completed" reference="TXN000009"/>
    <sms type="DEPOSIT" amount="15000" sender="0791234567" receiver="BANK" 
         timestamp="2024-01-19T11:20:00" status="completed" reference="TXN000010"/>
    <sms type="WITHDRAW" amount="3000" sender="ATM002" receiver="0791234567" 
         timestamp="2024-01-19T16:00:00" status="completed" reference="TXN000011"/>
    <sms type="SEND" amount="2500" sender="0791234567" receiver="0799999999" 
         timestamp="2024-01-20T09:30:00" status="completed" reference="TXN000012"/>
    <sms type="PAYMENT" amount="1200" sender="0791234567" receiver="SHOP_ABC" 
         timestamp="2024-01-20T13:15:00" status="completed" reference="TXN000013"/>
    <sms type="RECEIVE" amount="5500" sender="0794444444" receiver="0791234567" 
         timestamp="2024-01-20T18:00:00" status="completed" reference="TXN000014"/>
    <sms type="SEND" amount="7000" sender="0791234567" receiver="0793333333" 
         timestamp="2024-01-21T10:45:00" status="completed" reference="TXN000015"/>
    <sms type="DEPOSIT" amount="20000" sender="0791234567" receiver="BANK" 
         timestamp="2024-01-21T14:30:00" status="completed" reference="TXN000016"/>
    <sms type="PAYMENT" amount="900" sender="0791234567" receiver="RESTAURANT" 
         timestamp="2024-01-21T19:00:00" status="completed" reference="TXN000017"/>
    <sms type="SEND" amount="4500" sender="0791234567" receiver="0792222222" 
         timestamp="2024-01-22T08:15:00" status="completed" reference="TXN000018"/>
    <sms type="RECEIVE" amount="6000" sender="0791111111" receiver="0791234567" 
         timestamp="2024-01-22T11:30:00" status="completed" reference="TXN000019"/>
    <sms type="WITHDRAW" amount="2500" sender="ATM003" receiver="0791234567" 
         timestamp="2024-01-22T15:00:00" status="completed" reference="TXN000020"/>
    <sms type="PAYMENT" amount="3500" sender="0791234567" receiver="SUPERMARKET" 
         timestamp="2024-01-22T17:45:00" status="completed" reference="TXN000021"/>
    <sms type="SEND" amount="1800" sender="0791234567" receiver="0797777777" 
         timestamp="2024-01-23T09:00:00" status="completed" reference="TXN000022"/>
    <sms type="DEPOSIT" amount="12000" sender="0791234567" receiver="BANK" 
         timestamp="2024-01-23T13:30:00" status="completed" reference="TXN000023"/>
    <sms type="RECEIVE" amount="4800" sender="0796666666" receiver="0791234567" 
         timestamp="2024-01-23T16:15:00" status="completed" reference="TXN000024"/>
    <sms type="PAYMENT" amount="2200" sender="0791234567" receiver="GAS_STATION" 
         timestamp="2024-01-24T08:45:00" status="completed" reference="TXN000025"/>
</sms_records>
"""
    
    with open(filename, 'w') as f:
        f.write(xml_content)
    
    print(f"Created sample XML: {filename}")


if __name__ == '__main__':
    xml_file = 'modified_sms_v2.xml'
    
    if not os.path.exists(xml_file):
        print("XML file not found. Creating sample...")
        create_sample_xml(xml_file)
    
    transactions = parse_xml_to_json(xml_file)
    
    if transactions:
        print(f"\nSample transaction:")
        print(json.dumps(transactions[0], indent=2))

#!/usr/bin/env python3
"""
Data Structures & Algorithms Comparison
Compares Linear Search vs Dictionary Lookup for transaction retrieval
"""

import json
import time
import random
import os
import sys

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_transactions():
    """Load transactions from existing data sources"""
    data_sources = [
        'data/processed/dashboard.json',
        'data/transactions.json',
        '../data/transactions.json'
    ]
    
    for source in data_sources:
        if os.path.exists(source):
            try:
                with open(source, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and 'transactions' in data:
                        transactions = data['transactions']
                    elif isinstance(data, list):
                        transactions = data
                    else:
                        continue
                    if transactions:
                        print(f"[INFO] Loaded {len(transactions)} transactions from {source}")
                        return transactions
            except Exception as e:
                print(f"[WARN] Could not load {source}: {e}")
                continue
    
    print("[ERROR] No transaction data found. Run ETL pipeline or parse_xml.py first.")
    return []

def linear_search(transactions, target_id):
    for transaction in transactions:
        if str(transaction.get('id')) == str(target_id):
            return transaction
    return None

def build_dictionary(transactions):
    return {str(t.get('id')): t for t in transactions if 'id' in t}

def dictionary_lookup(transaction_dict, target_id):
    return transaction_dict.get(str(target_id))

def benchmark_searches(transactions, num_searches=1000):
    if not transactions:
        print("[ERROR] No transactions to benchmark")
        return None

    print(f"\n{'='*70}")
    print(f"BENCHMARKING {num_searches} SEARCHES")
    print(f"{'='*70}")
    print(f"Dataset Size: {len(transactions)} transactions\n")

    build_start = time.time()
    transaction_dict = build_dictionary(transactions)
    build_time = time.time() - build_start
    print(f"[INFO] Dictionary build time: {build_time*1000:.4f} ms\n")

    all_ids = [str(t.get('id')) for t in transactions if 'id' in t]
    search_ids = random.choices(all_ids, k=num_searches)

    # Linear search
    linear_start = time.time()
    linear_found = sum(1 for sid in search_ids if linear_search(transactions, sid))
    linear_time = time.time() - linear_start

    # Dictionary lookup
    dict_start = time.time()
    dict_found = sum(1 for sid in search_ids if dictionary_lookup(transaction_dict, sid))
    dict_time = time.time() - dict_start

    linear_avg = (linear_time / num_searches) * 1000
    dict_avg = (dict_time / num_searches) * 1000
    speedup = linear_time / dict_time if dict_time > 0 else 0

    return {
        'dataset_size': len(transactions),
        'num_searches': num_searches,
        'build_time_ms': build_time * 1000,
        'linear_total_ms': linear_time * 1000,
        'linear_avg_ms': linear_avg,
        'dict_total_ms': dict_time * 1000,
        'dict_avg_ms': dict_avg,
        'speedup': speedup,
        'linear_found': linear_found,
        'dict_found': dict_found
    }

def print_results(metrics):
    print(f"\n{'='*70}")
    print("PERFORMANCE COMPARISON RESULTS")
    print(f"{'='*70}\n")

    print(f"Dataset Size: {metrics['dataset_size']} transactions")
    print(f"Number of Searches: {metrics['num_searches']}")
    print(f"Dictionary Build Time: {metrics['build_time_ms']:.4f} ms\n")

    print("LINEAR SEARCH (O(n))")
    print(f"Total Time: {metrics['linear_total_ms']:.4f} ms")
    print(f"Average per Search: {metrics['linear_avg_ms']:.6f} ms")
    print(f"Results Found: {metrics['linear_found']}/{metrics['num_searches']}\n")

    print("DICTIONARY LOOKUP (O(1))")
    print(f"Total Time: {metrics['dict_total_ms']:.4f} ms")
    print(f"Average per Search: {metrics['dict_avg_ms']:.6f} ms")
    print(f"Results Found: {metrics['dict_found']}/{metrics['num_searches']}\n")

    print(f"Speedup: {metrics['speedup']:.2f}x faster with dictionary")
    print(f"Time Saved: {metrics['linear_total_ms'] - metrics['dict_total_ms']:.4f} ms")
    print("="*70 + "\n")

def save_results(metrics, filepath='dsa/results.txt'):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(f"DSA PERFORMANCE COMPARISON - TRANSACTION SEARCH\n")
        f.write(f"Dataset Size: {metrics['dataset_size']}\n")
        f.write(f"Number of Searches: {metrics['num_searches']}\n")
        f.write(f"Linear Total: {metrics['linear_total_ms']:.4f} ms\n")
        f.write(f"Dictionary Total: {metrics['dict_total_ms']:.4f} ms\n")
        f.write(f"Speedup: {metrics['speedup']:.2f}x\n")
    print(f"[INFO] Results saved to {filepath}")

if __name__ == '__main__':
    print("="*70)
    print("TRANSACTION SEARCH - DSA COMPARISON")
    print("="*70)

    transactions = load_transactions()
    if not transactions:
        sys.exit(1)

    if len(transactions) < 20:
        print(f"[WARN] Only {len(transactions)} transactions found. Benchmark may be less meaningful.")

    metrics = benchmark_searches(transactions, num_searches=1000)
    if metrics:
        print_results(metrics)
        save_results(metrics)

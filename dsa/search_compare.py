#!/usr/bin/env python3
"""
DSA Performance Comparison
Linear Search vs Dictionary Lookup
"""

import json
import time
import random
import os


def load_transactions(filepath='data/transactions.json'):
    """Load transactions from JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return []


def linear_search(transactions, target_id):
    """Linear Search - O(n) time complexity"""
    for transaction in transactions:
        if str(transaction.get('id')) == str(target_id):
            return transaction
    return None


def build_dictionary(transactions):
    """Build dictionary - O(n) time to build"""
    return {str(t.get('id')): t for t in transactions if 'id' in t}


def dictionary_lookup(transaction_dict, target_id):
    """Dictionary Lookup - O(1) average time complexity"""
    return transaction_dict.get(str(target_id))


def benchmark(transactions, num_searches=1000):
    """Compare performance of both search methods"""
    
    if not transactions:
        return None
    
    print(f"Dataset: {len(transactions)} transactions")
    print(f"Searches: {num_searches}\n")
    
    # Build dictionary
    build_start = time.time()
    transaction_dict = build_dictionary(transactions)
    build_time = time.time() - build_start
    
    # Generate random IDs
    all_ids = [str(t.get('id')) for t in transactions if 'id' in t]
    search_ids = random.choices(all_ids, k=num_searches)
    
    # Test Linear Search
    linear_start = time.time()
    for search_id in search_ids:
        linear_search(transactions, search_id)
    linear_time = time.time() - linear_start
    
    # Test Dictionary Lookup
    dict_start = time.time()
    for search_id in search_ids:
        dictionary_lookup(transaction_dict, search_id)
    dict_time = time.time() - dict_start
    
    return {
        'dataset_size': len(transactions),
        'num_searches': num_searches,
        'build_time_ms': build_time * 1000,
        'linear_total_ms': linear_time * 1000,
        'linear_avg_ms': (linear_time / num_searches) * 1000,
        'dict_total_ms': dict_time * 1000,
        'dict_avg_ms': (dict_time / num_searches) * 1000,
        'speedup': linear_time / dict_time if dict_time > 0 else 0
    }


def print_results(metrics):
    """Print formatted results"""
    
    print("="*70)
    print("PERFORMANCE COMPARISON RESULTS")
    print("="*70)
    print(f"\nDataset Size: {metrics['dataset_size']} transactions")
    print(f"Number of Searches: {metrics['num_searches']}")
    print(f"Dictionary Build Time: {metrics['build_time_ms']:.4f} ms\n")
    
    print("LINEAR SEARCH (O(n))")
    print(f"  Total Time: {metrics['linear_total_ms']:.4f} ms")
    print(f"  Average: {metrics['linear_avg_ms']:.6f} ms\n")
    
    print("DICTIONARY LOOKUP (O(1))")
    print(f"  Total Time: {metrics['dict_total_ms']:.4f} ms")
    print(f"  Average: {metrics['dict_avg_ms']:.6f} ms\n")
    
    print("="*70)
    print(f"Speedup: {metrics['speedup']:.2f}x faster")
    print(f"Time Saved: {metrics['linear_total_ms'] - metrics['dict_total_ms']:.4f} ms")
    print("="*70)


def save_results(metrics, filepath='dsa/results.txt'):
    """Save results to file"""
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        f.write("="*70 + "\n")
        f.write("DSA PERFORMANCE COMPARISON\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Dataset Size: {metrics['dataset_size']} transactions\n")
        f.write(f"Number of Searches: {metrics['num_searches']}\n")
        f.write(f"Dictionary Build Time: {metrics['build_time_ms']:.4f} ms\n\n")
        
        f.write("LINEAR SEARCH (O(n))\n")
        f.write(f"  Total Time: {metrics['linear_total_ms']:.4f} ms\n")
        f.write(f"  Average Time: {metrics['linear_avg_ms']:.6f} ms\n\n")
        
        f.write("DICTIONARY LOOKUP (O(1))\n")
        f.write(f"  Total Time: {metrics['dict_total_ms']:.4f} ms\n")
        f.write(f"  Average Time: {metrics['dict_avg_ms']:.6f} ms\n\n")
        
        f.write(f"SPEEDUP: {metrics['speedup']:.2f}x faster\n\n")
        
        f.write("="*70 + "\n")
        f.write("ANALYSIS\n")
        f.write("="*70 + "\n\n")
        
        f.write("Dictionary lookup is faster because:\n\n")
        f.write("1. Hash table provides O(1) average access time\n")
        f.write("2. Direct memory location via hash function\n")
        f.write("3. No iteration through entire list\n\n")
        
        f.write("Linear search must check each element sequentially (O(n)),\n")
        f.write("making it slower as dataset grows.\n\n")
        
        f.write("Alternative data structures:\n")
        f.write("- Binary Search Tree: O(log n)\n")
        f.write("- B-Tree: O(log n), optimized for databases\n")
        f.write("- Trie: O(k) for prefix searches\n")
    
    print(f"\nResults saved to {filepath}")


if __name__ == '__main__':
    print("="*70)
    print("DSA COMPARISON - TRANSACTION SEARCH")
    print("="*70 + "\n")
    
    transactions = load_transactions()
    
    if not transactions:
        print("No data found. Run: python dsa/xml_parser.py")
        exit(1)
    
    metrics = benchmark(transactions, num_searches=1000)
    
    if metrics:
        print_results(metrics)
        save_results(metrics)

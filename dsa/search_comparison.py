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
                        print(f"Loaded {len(transactions)} transactions from {source}")
                        return transactions
                        
            except Exception as e:
                continue
    
    print("No transaction data found. Run ETL pipeline or parse_xml.py first.")
    return []


def linear_search(transactions, target_id):
    """
    Linear Search Algorithm - O(n) time complexity
    Scans through list sequentially until match found
    """
    for transaction in transactions:
        if str(transaction.get('id')) == str(target_id):
            return transaction
    return None


def build_dictionary(transactions):
    """Build hash table (dictionary) from transactions - O(n) time"""
    return {str(t.get('id')): t for t in transactions if 'id' in t}


def dictionary_lookup(transaction_dict, target_id):
    """Dictionary Lookup - O(1) average time complexity"""
    return transaction_dict.get(str(target_id))


def benchmark_searches(transactions, num_searches=1000):
    """Compare performance of both search methods"""
    
    if not transactions:
        print("No transactions to benchmark")
        return None
    
    print(f"\n{'='*70}")
    print(f"BENCHMARKING {num_searches} SEARCHES")
    print(f"{'='*70}")
    print(f"Dataset Size: {len(transactions)} transactions\n")
    
    print("Building dictionary...")
    build_start = time.time()
    transaction_dict = build_dictionary(transactions)
    build_time = time.time() - build_start
    print(f"Build time: {build_time*1000:.4f} ms\n")
    
    all_ids = [str(t.get('id')) for t in transactions if 'id' in t]
    if not all_ids:
        print("No valid IDs found in transactions")
        return None
    
    search_ids = random.choices(all_ids, k=num_searches)
    
    print("Testing Linear Search (O(n))...")
    linear_start = time.time()
    linear_found = 0
    for search_id in search_ids:
        result = linear_search(transactions, search_id)
        if result:
            linear_found += 1
    linear_time = time.time() - linear_start
    print(f"  Completed: {linear_found}/{num_searches} found")
    
    print("\nTesting Dictionary Lookup (O(1))...")
    dict_start = time.time()
    dict_found = 0
    for search_id in search_ids:
        result = dictionary_lookup(transaction_dict, search_id)
        if result:
            dict_found += 1
    dict_time = time.time() - dict_start
    print(f"  Completed: {dict_found}/{num_searches} found")
    
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
    """Print formatted benchmark results"""
    
    print(f"\n{'='*70}")
    print("PERFORMANCE COMPARISON RESULTS")
    print(f"{'='*70}\n")
    
    print(f"Dataset Size: {metrics['dataset_size']} transactions")
    print(f"Number of Searches: {metrics['num_searches']}")
    print(f"Dictionary Build Time: {metrics['build_time_ms']:.4f} ms\n")
    
    print(f"{'-'*70}")
    print("LINEAR SEARCH")
    print(f"{'-'*70}")
    print(f"Algorithm: Sequential scan through list")
    print(f"Time Complexity: O(n)")
    print(f"Total Time: {metrics['linear_total_ms']:.4f} ms")
    print(f"Average per Search: {metrics['linear_avg_ms']:.6f} ms")
    print(f"Results Found: {metrics['linear_found']}/{metrics['num_searches']}")
    
    print(f"\n{'-'*70}")
    print("DICTIONARY LOOKUP")
    print(f"{'-'*70}")
    print(f"Algorithm: Direct hash table access")
    print(f"Time Complexity: O(1) average")
    print(f"Total Time: {metrics['dict_total_ms']:.4f} ms")
    print(f"Average per Search: {metrics['dict_avg_ms']:.6f} ms")
    print(f"Results Found: {metrics['dict_found']}/{metrics['num_searches']}")
    
    print(f"\n{'='*70}")
    print("COMPARISON SUMMARY")
    print(f"{'='*70}")
    print(f"Speedup: {metrics['speedup']:.2f}x faster with dictionary")
    print(f"Time Saved: {metrics['linear_total_ms'] - metrics['dict_total_ms']:.4f} ms")
    print(f"Percentage Improvement: {((metrics['speedup']-1)*100):.1f}%")
    print(f"{'='*70}\n")


def save_results(metrics, filepath='dsa/results.txt'):
    """Save detailed results to file"""
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        f.write("="*70 + "\n")
        f.write("DSA PERFORMANCE COMPARISON - TRANSACTION SEARCH\n")
        f.write("="*70 + "\n\n")
        
        f.write("BENCHMARK CONFIGURATION\n")
        f.write(f"Dataset Size: {metrics['dataset_size']} transactions\n")
        f.write(f"Number of Searches: {metrics['num_searches']}\n")
        f.write(f"Dictionary Build Time: {metrics['build_time_ms']:.4f} ms\n\n")
        
        f.write("LINEAR SEARCH (O(n))\n")
        f.write(f"  Total Time: {metrics['linear_total_ms']:.4f} ms\n")
        f.write(f"  Average Time: {metrics['linear_avg_ms']:.6f} ms per search\n")
        f.write(f"  Results Found: {metrics['linear_found']}/{metrics['num_searches']}\n")
        f.write(f"  Approach: Sequential iteration through list\n\n")
        
        f.write("DICTIONARY LOOKUP (O(1))\n")
        f.write(f"  Total Time: {metrics['dict_total_ms']:.4f} ms\n")
        f.write(f"  Average Time: {metrics['dict_avg_ms']:.6f} ms per search\n")
        f.write(f"  Results Found: {metrics['dict_found']}/{metrics['num_searches']}\n")
        f.write(f"  Approach: Hash table direct access\n\n")
        
        f.write(f"PERFORMANCE GAIN: {metrics['speedup']:.2f}x faster ({((metrics['speedup']-1)*100):.1f}% improvement)\n\n")
        
        f.write("="*70 + "\n")
        f.write("ANALYSIS\n")
        f.write("="*70 + "\n\n")
        
        f.write("Why is dictionary lookup faster?\n\n")
        
        f.write("1. HASH TABLE ACCESS:\n")
        f.write("   - Dictionary uses hash function to compute index\n")
        f.write("   - Direct memory location access\n")
        f.write("   - No iteration required\n\n")
        
        f.write("2. TIME COMPLEXITY:\n")
        f.write("   - Linear Search: O(n) - time grows with dataset\n")
        f.write("   - Dictionary: O(1) - constant time\n\n")
        
        f.write("3. REAL-WORLD IMPACT:\n")
        f.write(f"   - Saved {metrics['linear_total_ms'] - metrics['dict_total_ms']:.4f} ms total\n")
        f.write(f"   - {((metrics['speedup']-1)*100):.1f}% performance improvement\n\n")
        
        f.write("TRADE-OFFS:\n")
        f.write("- Dictionary requires O(n) space\n")
        f.write("- Dictionary needs initial build time\n")
        f.write("- Worth it for multiple searches\n\n")
        
        f.write("OTHER EFFICIENT DATA STRUCTURES:\n\n")
        
        f.write("1. BINARY SEARCH TREE:\n")
        f.write("   - Time: O(log n) if balanced\n")
        f.write("   - Good for range queries\n\n")
        
        f.write("2. B-TREE:\n")
        f.write("   - Time: O(log n)\n")
        f.write("   - Optimized for disk access\n")
        f.write("   - Used in databases\n\n")
        
        f.write("3. TRIE:\n")
        f.write("   - Time: O(k) where k = key length\n")
        f.write("   - Good for prefix searches\n\n")
        
        f.write("RECOMMENDATION:\n")
        f.write("Dictionary (hash table) is optimal for ID-based lookups.\n")
        f.write("Provides O(1) average access with minimal overhead.\n")
    
    print(f"Detailed results saved to {filepath}")


if __name__ == '__main__':
    print("="*70)
    print("TRANSACTION SEARCH - DSA COMPARISON")
    print("="*70)
    
    transactions = load_transactions()
    
    if not transactions:
        print("\nNo data found.")
        print("Run: python etl/run.py or python etl/parse_xml.py")
        sys.exit(1)
    
    if len(transactions) < 20:
        print(f"\nWarning: Only {len(transactions)} transactions found")
        print("Assignment requires at least 20 for comparison")
    
    metrics = benchmark_searches(transactions, num_searches=1000)
    
    if metrics:
        print_results(metrics)
        save_results(metrics)
        
        print(f"\nDSA comparison complete!")
        print(f"Dictionary is {metrics['speedup']:.2f}x faster than linear search")
    else:
        print("\nBenchmark failed")
        sys.exit(1)

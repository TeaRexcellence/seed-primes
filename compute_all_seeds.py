#!/usr/bin/env python3
"""
Extended computation script with checkpointing for long runs
Useful for verifying no seed primes exist beyond 167 up to very large limits

Author: Ian Shannon-Garvey
Date: July 2025
"""

# ADJUST THIS VALUE TO SET YOUR SEARCH LIMIT
SEARCH_LIMIT = 10000  # Default: search up to 10,000

import json
import time
import os
from datetime import datetime

# Standard implementation
def is_prime(n):
    """Check if n is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_seed_prime(n):
    """Check if prime n cannot be written as a + 2*b with a < b both prime"""
    if not is_prime(n):
        return False
    
    for a in range(2, n//3 + 1):
        if is_prime(a):
            remainder = n - a
            if remainder % 2 == 0:
                b = remainder // 2
                if b > a and is_prime(b):
                    return False
    return True

def compute_with_checkpointing(limit, checkpoint_interval=1000000):
    """Compute seed primes with checkpointing for recovery"""
    checkpoint_file = f"seed_primes_checkpoint_{limit}.json"
    
    # Try to load checkpoint
    start_from = 2
    seeds_found = []
    
    if os.path.exists(checkpoint_file):
        print(f"Loading checkpoint from {checkpoint_file}")
        with open(checkpoint_file, 'r') as f:
            data = json.load(f)
            start_from = data['last_checked'] + 1
            seeds_found = data['seeds_found']
            print(f"Resuming from {start_from:,}")
    
    # Continue computation
    last_checkpoint = start_from
    start_time = time.time()
    
    try:
        for n in range(start_from, limit + 1):
            if is_seed_prime(n):
                seeds_found.append(n)
                print(f"Found seed prime: {n}")
            
            # Checkpoint periodically
            if n - last_checkpoint >= checkpoint_interval or n == limit:
                with open(checkpoint_file, 'w') as f:
                    json.dump({
                        'last_checked': n,
                        'seeds_found': seeds_found,
                        'timestamp': datetime.now().isoformat()
                    }, f)
                
                elapsed = time.time() - start_time
                rate = (n - start_from + 1) / elapsed
                remaining = (limit - n) / rate if rate > 0 else 0
                
                print(f"Checkpoint at {n:,} ({n/limit*100:.1f}%)")
                print(f"  Seeds found: {len(seeds_found)}")
                print(f"  Rate: {rate:.0f} numbers/second")
                print(f"  ETA: {remaining/60:.1f} minutes")
                
                last_checkpoint = n
    
    except KeyboardInterrupt:
        print("\nInterrupted. Progress saved to checkpoint.")
        return seeds_found
    
    # Clean up checkpoint file on completion
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)
    
    return seeds_found

def verify_generation_claim(seeds, limit):
    """Verify that seeds generate all primes up to limit"""
    print(f"\nVerifying that {len(seeds)} seeds generate all primes up to {limit}")
    
    generated = set(seeds)
    generation = 0
    
    while True:
        new_found = False
        generation += 1
        current = sorted(list(generated))
        
        for p in current:
            for q in current:
                if p < q:
                    r = p + 2 * q
                    if r <= limit and r not in generated and is_prime(r):
                        generated.add(r)
                        new_found = True
        
        if not new_found:
            break
        
        print(f"Generation {generation}: {len(generated)} primes total")
    
    # Check coverage
    actual_primes = [n for n in range(2, limit + 1) if is_prime(n)]
    coverage = len(generated & set(actual_primes)) / len(actual_primes) * 100
    
    print(f"\nCoverage: {coverage:.1f}% ({len(generated)}/{len(actual_primes)} primes)")
    
    if coverage < 100:
        missed = sorted(set(actual_primes) - generated)[:10]
        print(f"Missed primes: {missed}...")
    
    return coverage == 100

def main():
    print("Extended Seed Prime Computation with Checkpointing")
    print("=" * 60)
    print(f"Search limit: {SEARCH_LIMIT:,}")
    
    # Quick test to verify implementation
    print("\nQuick verification up to 1000...")
    seeds_1k = [n for n in range(2, 1001) if is_seed_prime(n)]
    print(f"Seeds found: {seeds_1k}")
    print(f"Expected: [2, 3, 5, 7, 11, 23, 83, 167]")
    print(f"Match: {seeds_1k == [2, 3, 5, 7, 11, 23, 83, 167]}")
    
    # Verify generation claim
    if verify_generation_claim(seeds_1k, 1000):
        print("Confirmed: These seeds generate all primes up to 1000.")
    
    # Main computation
    print(f"\n\nStarting search for seed primes up to {SEARCH_LIMIT:,}...")
    print("Press Ctrl+C at any time to pause (progress will be saved)")
    print("-" * 60)
    
    # Determine checkpoint interval based on limit
    if SEARCH_LIMIT <= 1000000:
        checkpoint_interval = 100000
    elif SEARCH_LIMIT <= 10000000:
        checkpoint_interval = 1000000
    else:
        checkpoint_interval = 5000000
    
    start_time = time.time()
    seeds = compute_with_checkpointing(SEARCH_LIMIT, checkpoint_interval)
    total_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print(f"\nSearch complete!")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"\nSeed primes found: {seeds}")
    
    if seeds == [2, 3, 5, 7, 11, 23, 83, 167]:
        print("\n✓ Confirmed: No seed primes exist beyond 167 up to {:,}".format(SEARCH_LIMIT))
    else:
        print("\n⚠ WARNING: Unexpected result! Found different seed primes.")

if __name__ == "__main__":
    main()
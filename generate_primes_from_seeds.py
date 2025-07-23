#!/usr/bin/env python3
"""
Prime generation using the 8 seed primes
Shows that {2, 3, 5, 7, 11, 23, 83, 167} generate all primes via r = p + 2q (p < q)

Author: Ian Shannon-Garvey
Date: July 2025
"""

# ADJUST THIS VALUE TO CHANGE THE VERIFICATION LIMIT
VERIFY_LIMIT = 10000  # Generate and verify primes up to this value

def is_prime(n):
    """Check if n is prime"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def verify_seed_generation_efficient(limit):
    """Efficiently verify that the 8 seed primes generate all other primes"""
    seeds = [2, 3, 5, 7, 11, 23, 83, 167]
    
    print(f"Verifying seed prime generation up to {limit:,}")
    print(f"Seed primes: {seeds}")
    print("-" * 60)
    
    # Get all primes up to limit
    all_primes_list = [p for p in range(2, limit + 1) if is_prime(p)]
    all_primes_set = set(all_primes_list)
    
    # Track which primes we can generate
    generated = set(seeds)  # Start with seeds
    generation_info = {}
    
    # Keep track of which generation each prime was found in
    for seed in seeds:
        if seed <= limit:
            generation_info[seed] = (0, None)  # Generation 0, no parents
    
    generation = 0
    new_found = True
    
    while new_found:
        new_found = False
        generation += 1
        current_gen = sorted(list(generated))
        new_in_generation = []
        
        # Try all combinations p + 2q with p < q from already generated primes
        for i, p in enumerate(current_gen):
            for j, q in enumerate(current_gen):
                if p < q:  # Strict inequality
                    r = p + 2 * q
                    if r > limit:
                        break  # No point checking further
                    if r in all_primes_set and r not in generated:
                        generated.add(r)
                        generation_info[r] = (generation, (p, q))
                        new_in_generation.append(r)
                        new_found = True
        
        if new_in_generation:
            print(f"Generation {generation}: Found {len(new_in_generation)} new primes")
            if len(new_in_generation) <= 10:
                print(f"  Examples: {sorted(new_in_generation[:10])}")
    
    # Calculate coverage
    primes_up_to_limit = [p for p in all_primes_list if p <= limit]
    coverage = len(generated & set(primes_up_to_limit)) / len(primes_up_to_limit) * 100
    
    # Find which primes weren't generated
    not_generated = [p for p in primes_up_to_limit if p not in generated]
    
    print(f"\nResults:")
    print(f"Total primes up to {limit:,}: {len(primes_up_to_limit)}")
    print(f"Generated (including seeds): {len([p for p in generated if p <= limit])}")
    print(f"Coverage: {coverage:.2f}%")
    
    if not_generated:
        print(f"\nERROR: {len(not_generated)} primes were not generated!")
        print(f"Missing primes: {not_generated[:20]}...")
    else:
        print(f"\n✓ SUCCESS: All {len(primes_up_to_limit)} primes up to {limit:,} were generated!")
    
    # Show some generation examples
    print(f"\nExample generations:")
    examples_shown = 0
    for p in sorted(all_primes_list):
        if p in generation_info and generation_info[p][1] is not None:
            gen, (parent_p, parent_q) = generation_info[p]
            print(f"{p} = {parent_p} + 2×{parent_q} (generation {gen})")
            examples_shown += 1
            if examples_shown >= 10:
                break
    
    return coverage == 100, generation_info

def analyze_generation_patterns(limit, generation_info):
    """Analyze patterns in how primes are generated"""
    print("\n\nGeneration Pattern Analysis")
    print("=" * 60)
    
    all_primes = [p for p in range(2, limit + 1) if is_prime(p)]
    
    # Count parent options for each prime
    parent_counts = {}
    for p in all_primes:
        if p > 167:  # Beyond seed primes
            count = 0
            for p1 in all_primes:
                if p1 >= p:
                    break
                remainder = p - p1
                if remainder % 2 == 0:
                    p2 = remainder // 2
                    if p2 > p1 and is_prime(p2) and p2 <= p:
                        count += 1
            parent_counts[p] = count
    
    # Find unique and hub primes
    unique_primes = [p for p, count in parent_counts.items() if count == 1]
    hub_primes = [(p, count) for p, count in parent_counts.items() if count > 5]
    hub_primes.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Analysis up to {limit:,}:")
    print(f"  Unique primes (only 1 parent pair): {len(unique_primes)}")
    if unique_primes[:10]:
        print(f"    First 10: {unique_primes[:10]}")
    
    print(f"  Hub primes (>5 parent pairs): {len(hub_primes)}")
    if hub_primes[:5]:
        print(f"    Top 5 hubs:")
        for p, count in hub_primes[:5]:
            print(f"      {p}: {count} parent pairs")
    
    # Generation depth analysis
    if generation_info:
        max_gen = max(g[0] for g in generation_info.values() if g[0] is not None)
        print(f"\n  Maximum generation depth: {max_gen}")
        for gen in range(max_gen + 1):
            count = len([p for p, (g, _) in generation_info.items() if g == gen])
            print(f"    Generation {gen}: {count} primes")

def main():
    print("8 Seed Prime Generation Verification")
    print("=" * 60)
    
    # Main verification
    success, generation_info = verify_seed_generation_efficient(VERIFY_LIMIT)
    
    # Pattern analysis
    if success:
        analyze_generation_patterns(VERIFY_LIMIT, generation_info)
    
    print("\n" + "=" * 60)
    print("Note: Set VERIFY_LIMIT at top of file to test larger ranges")

if __name__ == "__main__":
    main()
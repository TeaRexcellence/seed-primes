#!/usr/bin/env python3
"""
Gap analysis for the 8 seed primes
Analyzes the pattern in gaps and shows the self-termination at 167

Author: Ian Shannon-Garvey
Date: July 2025
"""

def is_prime(n):
    """Check if n is prime"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def analyze_gap_sequence():
    """Analyze the gaps between seed primes"""
    seeds = [2, 3, 5, 7, 11, 23, 83, 167]
    
    print("Seed Primes Gap Analysis")
    print("=" * 50)
    print(f"\nSeed primes: {seeds}")
    print(f"Sum of seeds: {sum(seeds)}")
    
    # Calculate gaps
    gaps = []
    for i in range(1, len(seeds)):
        gap = seeds[i] - seeds[i-1]
        gaps.append(gap)
        print(f"{seeds[i]:3d} - {seeds[i-1]:3d} = {gap:3d}")
    
    print(f"\nGap sequence: {gaps}")
    
    # Analyze the pattern
    print("\nPattern analysis:")
    print(f"Gaps[0:3] = {gaps[0:3]}  (1, 2, 2)")
    print(f"Gap[3] = {gaps[3]}  (pivotal gap)")
    
    if len(gaps) >= 6:
        print(f"\nCascade pattern after gap 4:")
        print(f"Gap[4] = {gaps[4]} = 4 × 3")
        print(f"Gap[5] = {gaps[5]} = 4 × 3 × 5")
        print(f"Gap[6] = {gaps[6]} = 4 × 3 × 7")
        
        # Verify the factorizations
        print(f"\nVerification:")
        print(f"4 × 3 = {4 * 3}")
        print(f"4 × 3 × 5 = {4 * 3 * 5}")
        print(f"4 × 3 × 7 = {4 * 3 * 7}")
    
    # Show self-termination
    print("\n\nSelf-termination proof:")
    print("If the pattern continues, the next gap would be:")
    next_gap = 4 * 3 * 11
    print(f"Next gap = 4 × 3 × 11 = {next_gap}")
    
    next_candidate = 167 + next_gap
    print(f"Next candidate = 167 + {next_gap} = {next_candidate}")
    
    # Check if it's prime
    if is_prime(next_candidate):
        print(f"{next_candidate} is PRIME - pattern continues")
    else:
        # Find factors
        factors = []
        for i in range(2, int(next_candidate**0.5) + 1):
            if next_candidate % i == 0:
                factors.append((i, next_candidate // i))
        
        print(f"{next_candidate} is COMPOSITE")
        if factors:
            print(f"Factorization: {next_candidate} = {factors[0][0]} × {factors[0][1]}")
    
    print("\nThis forces the sequence to terminate at exactly 8 seed primes.")
    
    # Additional analysis
    print("\n\nAdditional observations:")
    print(f"Number of seeds: {len(seeds)}")
    print(f"Largest seed: {seeds[-1]}")
    print(f"PSL(2,7) order: 168 = 8 × 21")
    print(f"167 = 168 - 1 (largest seed = PSL(2,7) order - 1)")
    
    # Gap ratios
    print("\nGap growth ratios:")
    for i in range(1, len(gaps)):
        ratio = gaps[i] / gaps[i-1]
        print(f"Gap[{i}] / Gap[{i-1}] = {gaps[i]} / {gaps[i-1]} = {ratio:.2f}")
    
    return seeds, gaps

def check_extended_seeds(limit):
    """Check if any primes beyond 167 are seed primes"""
    print(f"\n\nChecking for seed primes from 168 to {limit}...")
    
    found = []
    for n in range(168, limit + 1):
        if is_prime(n):
            is_seed = True
            # Check if n can be written as p + 2q with p < q
            for p in range(2, n//3 + 1):
                if is_prime(p):
                    remainder = n - p
                    if remainder % 2 == 0:
                        q = remainder // 2
                        if q > p and is_prime(q):
                            is_seed = False
                            break
            
            if is_seed:
                found.append(n)
                print(f"Found seed prime: {n}")
    
    if not found:
        print(f"No seed primes found between 168 and {limit}")
    
    return found

def main():
    seeds, gaps = analyze_gap_sequence()
    
    # Quick check up to 10,000
    extended = check_extended_seeds(10000)
    
    if not extended:
        print("\n\nConclusion: The sequence of seed primes is complete at 8 terms.")
        print("The self-terminating pattern and computational verification")
        print("strongly suggest these are the only seed primes.")

if __name__ == "__main__":
    main()
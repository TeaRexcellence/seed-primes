#!/usr/bin/env python3
"""Quick test of the seed prime scripts"""

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_seed_prime(n):
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

# Test 1: Find seed primes up to 200
print("Test 1: Finding seed primes up to 200")
seeds = [n for n in range(2, 201) if is_seed_prime(n)]
print(f"Seed primes: {seeds}")
print(f"Expected: [2, 3, 5, 7, 11, 23, 83, 167]")
print(f"Match: {seeds == [2, 3, 5, 7, 11, 23, 83, 167]}")

# Test 2: Verify non-seeds have representations
print("\nTest 2: Verifying non-seed examples")
non_seeds = [13, 17, 19, 29, 37]
for p in non_seeds:
    for a in range(2, p//3 + 1):
        if is_prime(a):
            remainder = p - a
            if remainder % 2 == 0:
                b = remainder // 2
                if b > a and is_prime(b):
                    print(f"{p} = {a} + 2×{b}")
                    break

# Test 3: Generate primes from seeds
print("\nTest 3: Generate primes from seeds up to 50")
seeds = [2, 3, 5, 7, 11, 23, 83, 167]
primes = set(seeds)
for p in seeds:
    for q in seeds:
        if p < q:
            r = p + 2*q
            if r <= 50 and is_prime(r):
                primes.add(r)
                print(f"{r} = {p} + 2×{q}")

generated = sorted(list(primes))
actual = [n for n in range(2, 51) if is_prime(n)]
print(f"\nGenerated: {[p for p in generated if p <= 50]}")
print(f"Actual:    {actual}")
print(f"Coverage: {len(set(generated) & set(actual))}/{len(actual)}")

# Test 4: Gap analysis
print("\nTest 4: Gap analysis")
seeds = [2, 3, 5, 7, 11, 23, 83, 167]
gaps = [seeds[i] - seeds[i-1] for i in range(1, len(seeds))]
print(f"Gaps: {gaps}")
print(f"Pattern check: 12 = 4×3 = {4*3}, 60 = 4×3×5 = {4*3*5}, 84 = 4×3×7 = {4*3*7}")
print(f"Next would be: 167 + 4×3×11 = 167 + {4*3*11} = {167 + 4*3*11}")
print(f"Is 299 prime? {is_prime(299)}")
if not is_prime(299):
    print(f"299 = 13 × 23")
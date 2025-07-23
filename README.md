# OEIS A385077: Seed Primes

This repository contains verification code for OEIS sequence A385077.

## Definition

**Seed primes**: Primes p that cannot be written as p = a + 2*b where a < b are primes.

The complete sequence: **2, 3, 5, 7, 11, 23, 83, 167**

## Key Properties

1. **Finite sequence**: Computational verification to 10^8 found no additional terms
2. **Self-terminating**: The gap pattern forces termination at 167
3. **Prime generators**: These 8 primes can generate all other primes via the rule r = p + 2q (p < q)

## Scripts

1. **`verify_seed_primes.py`** - Main verification script
   - Verifies the definition of seed primes
   - Searches for seed primes up to any specified limit
   - Shows examples of how non-seed primes can be decomposed
   - No dependencies required

2. **`generate_primes_from_seeds.py`** - Prime generation demonstration
   - Shows that the 8 seed primes generate all other primes
   - Uses the rule: r = p + 2q where p < q (strict inequality)
   - Verifies 100% coverage of all primes up to specified limit
   - Analyzes "hub" vs "unique" primes based on number of parent pairs

3. **`gap_analysis.py`** - Gap sequence analysis
   - Analyzes the gaps between consecutive seed primes
   - Shows the cascade pattern: 12 = 4×3, 60 = 4×3×5, 84 = 4×3×7
   - Proves self-termination: next would be 167 + 132 = 299 = 13×23 (composite)

4. **`compute_all_seeds.py`** - Extended computation with checkpointing
   - Searches for seed primes with checkpoint/resume support
   - Useful for verification to large limits (10^8 and beyond)
   - Saves progress to avoid losing work on interruption

5. **`quick_test.py`** - Quick functionality test
   - Runs basic tests of all core functions
   - Good for verifying installation and basic functionality

## Running the Code

All scripts have configurable limits at the top of each file. Simply edit the constants to change search ranges.

```bash
# Verify the 8 seed primes (default: searches to 1,000,000)
python3 verify_seed_primes.py

# Show how they generate all primes (default: up to 10,000)
python3 generate_primes_from_seeds.py

# Analyze the gap pattern
python3 gap_analysis.py

# Extended verification with checkpointing (for searches to 10^8+)
python3 compute_all_seeds.py

# Quick test of all functionality
python3 quick_test.py
```

## Mathematical Significance

These 8 primes form a minimal generating set for all primes under the rule r = p + 2q (with p < q). The self-terminating gap pattern and extensive computational verification to 10^8 confirm this sequence is complete.

Iterative application of p + 2q (strict inequality: p < q) starting from just these 8 primes generates every prime number.

## References

- Juhász, Z., Bartalos, M., Magyar, P., & Farkas, G. (2023). Empirical verification of a new generalisation of Goldbach's conjecture up to 10^{12} (or 10^{13}) for all coefficients <= 40. arXiv:2304.00024

## Author

Ian Shannon-Garvey (2025)
from itertools import combinations_with_replacement, permutations
from collections import Counter

def analyze_shapes():
    # Generate all 560 unique distributions
    all_dist = []
    for s, sh, shd in combinations_with_replacement(range(14), 3):
        all_dist.append((s, sh - s, shd - sh, 13 - shd))
    
    print(f"Total distributions generated: {len(all_dist)}")
    
    # Group them by type (partition of 13)
    types = {}
    for d in all_dist:
        t = tuple(sorted(d, reverse=True))
        if t not in types:
            types[t] = []
        types[t].append(d)
        
    print(f"Total unique types: {len(types)}")
    
    # Calculate permutations for each type
    results = []
    for t, distributions in types.items():
        # How many permutations does this type have?
        # A type like (4,3,3,3) has 4 permutations.
        # The number of distributions for this type in our list should match this.
        n_perms = len(distributions)
        results.append((t, n_perms))
        
    # Group results by number of permutations and list types
    summary = {} # n_perms -> [types]
    for t, n_perms in results:
        if n_perms not in summary:
            summary[n_perms] = []
        summary[n_perms].append(t)
        
    print("\nDetailed breakdown:")
    total_shapes = 0
    total_dist = 0
    for n_perms in sorted(summary.keys()):
        types_list = summary[n_perms]
        count = len(types_list)
        prod = n_perms * count
        print(f"\nPermutations: {n_perms} ({count} shapes, total {prod})")
        print("  " + ", ".join([str(t) for t in sorted(types_list, reverse=True)]))
        total_shapes += count
        total_dist += prod
        
    print("-" * 50)
    print(f"Total        | {total_shapes:16} | {total_dist:18}")

if __name__ == "__main__":
    analyze_shapes()

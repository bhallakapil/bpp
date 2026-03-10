from math import comb
from collections import Counter

def calculate_theoretical_probability(shape):
    """
    Calculates the probability of a hand having a specific shape.
    shape: sorted tuple of suit lengths, e.g. (4, 4, 3, 2)
    """
    # Number of ways to choose these card counts from each suit
    ways = 1
    for count in shape:
        ways *= comb(13, count)
        
    # Total number of ways to pick 13 cards from 52
    total_hands = comb(52, 13)
    
    # Account for permutations (how many ways to assign these lengths to suits)
    counts = Counter(shape)
    permutations = 24 # 4!
    for multiplicity in counts.values():
        if multiplicity == 2: permutations //= 2
        elif multiplicity == 3: permutations //= 6
        elif multiplicity == 4: permutations //= 24
        
    return (ways * permutations) / total_hands

balanced = [(4, 4, 3, 2), (5, 3, 3, 2), (4, 3, 3, 3)]
semi_balanced = [(5, 4, 2, 2), (6, 3, 2, 2)]
singleton_shapes = [(5, 4, 3, 1), (6, 4, 2, 1), (6, 3, 3, 1), (5, 5, 2, 1), (4, 4, 4, 1)]

print("Balanced Shapes:")
total_balanced = 0
for s in balanced:
    p = calculate_theoretical_probability(s)
    total_balanced += p
    print(f"  {'-'.join(map(str, s))}: {p*100:6.2f}%")
print(f"Total Balanced: {total_balanced*100:6.2f}%")

print("\nSemi-Balanced Shapes:")
total_semi = 0
for s in semi_balanced:
    p = calculate_theoretical_probability(s)
    total_semi += p
    print(f"  {'-'.join(map(str, s))}: {p*100:6.2f}%")
print(f"Total Semi-Balanced: {total_semi*100:6.2f}%")

print("\nSingleton Shapes (requested):")
total_singleton = 0
for s in singleton_shapes:
    p = calculate_theoretical_probability(s)
    total_singleton += p
    print(f"  {'-'.join(map(str, s))}: {p*100:6.2f}%")
print(f"Total Singleton requested: {total_singleton*100:6.2f}%")

print(f"\nCombined Total (Bal + Semi): {(total_balanced + total_semi)*100:6.2f}%")
print(f"Grand Total (All above): {(total_balanced + total_semi + total_singleton)*100:6.2f}%")

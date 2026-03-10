from collections import Counter, defaultdict
from math import comb
from redeal import bigdeal, Hand
import time

def get_normalized_shape(hand):
    return tuple(sorted(hand.shape, reverse=True))

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
    # 4! / (product of factorials of multiplicities of lengths)
    counts = Counter(shape)
    permutations = 24 # 4!
    for multiplicity in counts.values():
        if multiplicity == 2: permutations //= 2
        elif multiplicity == 3: permutations //= 6
        elif multiplicity == 4: permutations //= 24
        
    return (ways * permutations) / total_hands

def run_simulation(n=10000000):
    counts = Counter()
    start_time = time.time()
    
    batch_size = 100000
    for i in range(0, n // 4, batch_size // 4):
        actual_batch = min(batch_size // 4, (n // 4) - i)
        for j in range(actual_batch):
            deal = bigdeal.get_deal(boardno=i+j)
            for card_list in deal:
                hand = Hand(card_list)
                counts[get_normalized_shape(hand)] += 1
        
        current_done = (i + actual_batch) * 4
        elapsed = time.time() - start_time
        rate = current_done / elapsed if elapsed > 0 else 0
        print(f"\rGenerated {current_done:,}/{n:,} hands ({rate:,.0f} hands/sec)...", end="", flush=True)
            
    end_time = time.time()
    print("\n" + "=" * 80)
    print(f"Simulation of {n:,} hands complete in {end_time - start_time:.2f}s")
    print("=" * 80)
    
    # Sort by frequency
    sorted_shapes = counts.most_common()
    
    header = f"{'Shape':<10} | {'Count':<10} | {'Actual %':<10} | {'Theo %':<10} | {'Deviance':<10}"
    print(header)
    print("-" * 80)
    
    for shape, count in sorted_shapes:
        actual_pct = (count / n) * 100
        theo_pct = calculate_theoretical_probability(shape) * 100
        deviance = abs(actual_pct - theo_pct)
        
        shape_str = "-".join(map(str, shape))
        print(f"{shape_str:<10} | {count:<10} | {actual_pct:>8.4f}% | {theo_pct:>8.4f}% | {deviance:>8.6f}%")

if __name__ == "__main__":
    run_simulation(10000000)

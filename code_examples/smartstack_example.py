import sys
import os
import time
from collections import Counter

# Add parent directory to sys.path to allow importing redeal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redeal import SmartStack, Shape, hcp, Hand, Card, Rank, Suit

def run_smartstack_analysis():
    """
    Demonstrates the efficiency and constraints of SmartStack.
    SmartStack pre-calculates valid holdings for a hand to satisfy
    shape and evaluation (HCP) constraints, allowing fast generation.
    """
    # 1. Configuration: 5-3-3-2 any order, 15-17 HCP
    shape = Shape("(5332)")
    hcp_range = range(15, 18)
    
    print(f"Setting up SmartStack for:")
    print(f"  Shape: {shape} (5-3-3-2 in any suit order)")
    print(f"  Evaluation: 15-17 HCP")
    
    # Initialize SmartStack
    ss = SmartStack(shape, hcp, hcp_range)
    
    # Pre-calculating takes some time
    start_init = time.time()
    # The first call triggers _prepare()
    _ = ss()
    end_init = time.time()
    print(f"Initialization (pre-calculating valid combinations) took {end_init - start_init:.4f}s")
    
    # 2. Generation benchmark
    n = 10000
    print(f"\nGenerating {n:,} hands...")
    
    shapes_found = Counter()
    hcp_found = Counter()
    
    start_gen = time.time()
    for _ in range(n):
        # ss() returns a list of Card objects
        hand_cards = ss()
        hand = Hand(hand_cards)
        
        # Track found shapes (normalized) and HCP
        shapes_found[tuple(sorted(hand.shape, reverse=True))] += 1
        hcp_found[hand.hcp] += 1
        
    end_gen = time.time()
    rate = n / (end_gen - start_gen)
    print(f"Generation complete in {end_gen - start_gen:.4f}s ({rate:,.0f} hands/sec)")
    
    # 3. Results verification
    print("\nVerified Shape distribution (expect 100% (5, 3, 3, 2)):")
    for s, count in shapes_found.items():
        print(f"  {s}: {count/n*100:.1f}% ({count})")
        
    print("\nVerified HCP distribution (expect 15-17 only):")
    for h, count in sorted(hcp_found.items()):
        print(f"  {h} HCP: {count/n*100:.1f}% ({count})")

    # 4. Using predealt cards
    print(f"\nExample with predealt Ace of Spades (AS) - meaning AS is ALREADY dealt elsewhere:")
    as_card = Card.from_str("SA")
    ss_no_as = SmartStack(shape, hcp, hcp_range, predealt={as_card})
    # Pre-calculate again for this specific constraint
    _ = ss_no_as()
    
    hand_without_as = Hand(ss_no_as())
    print(f"Generated hand: {hand_without_as}")
    print(f"Contains AS? {as_card in hand_without_as} (Expected: False)")
    print(f"HCP: {hand_without_as.hcp}")
    print(f"Shape: {hand_without_as.shape}")

if __name__ == "__main__":
    run_smartstack_analysis()

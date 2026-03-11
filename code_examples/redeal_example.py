import sys
import os

# Add parent directory to sys.path to allow importing redeal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redeal import (
    Hand, Deal, Shape, Contract, 
    hcp, qp, controls, Evaluator,
    balanced, semibalanced,
    Seat, Suit, Rank
)

def demonstrate_redeal_core():
    print("--- 1. Hands and Cards ---")
    # Create a hand from string
    # Suit order: Spades Hearts Diamonds Clubs
    h1 = Hand.from_str("AK432 K87 QJT54 -")
    print(f"Hand 1: {h1}")
    print(f"  Spades: {h1.spades}")
    print(f"  Shape: {h1.shape}")
    print(f"  HCP: {h1.hcp}")
    print(f"  Is 1NT opener? {h1.is_1nt}")

    print("\n--- 2. Shape Constraints ---")
    # Shape strings use ( ) for permutations and x for any length
    # (4333) means any suit order of 4-3-3-3
    s1 = Shape("(4333)")
    print(f"Is Hand 1 {s1}? {s1(h1)}")
    
    # Predefined shapes
    print(f"Is Hand 1 balanced? {balanced(h1)}")
    print(f"Is Hand 1 semibalanced? {semibalanced(h1)}")

    print("\n--- 3. Dealing ---")
    # Prepare a dealer where North is fixed
    fixed_north = "AKQJ T98 765 432" # 10 HCP
    
    predeal = {
        "N": fixed_north
    }
    
    dealer = Deal.prepare(predeal)
    
    # Generate a deal with a requirement for South's HCP
    def south_is_strong(deal):
        return deal.south.hcp >= 15

    deal = dealer(accept_func=south_is_strong) 
    
    Deal.set_str_style("long")
    print(f"Generated Deal where South has >= 15 HCP:\n{deal}")
    print(f"South HCP: {deal.south.hcp}")

    print("\n--- 4. Contracts and Scoring ---")
    # Create a contract (3NT)
    # level, strain, doubled (0,1,2), vul (True/False)
    c = Contract(3, "N", doubled=0, vul=True)
    print(f"Contract: {c}")
    
    # Score it for 10 tricks (3NT + 1)
    score = c.score(10)
    print(f"Score for 10 tricks: {score}")
    
    # Score for 8 tricks (3NT - 1)
    print(f"Score for 8 tricks: {c.score(8)}")

    print("\n--- 5. Evaluation ---")
    # Evaluators can be used on holdings or hands
    # qp (Quick Points), controls, etc.
    print(f"Hand 1 QP: {h1.qp}")
    print(f"Hand 1 Controls: {h1.controls}")

    # Custom evaluator (e.g., 1-Ace, 0-others)
    ace_eval = Evaluator(1, 0, 0, 0)
    print(f"Hand 1 Ace count: {ace_eval(h1)}")

if __name__ == "__main__":
    demonstrate_redeal_core()

import sys
import os

# Add parent directory to sys.path to allow importing redeal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redeal import bigdeal, Hand, Suit, Rank

def run_bigdeal_example():
    """
    Demonstrates bigdeal.py functionality:
    - Deterministic board generation
    - Partial deal generation
    - bigdeal standard mapping algorithm
    """
    
    # 1. Standard Board Generation
    # Generates a deal based on board number, entropy (OS-based), and owner name
    # This is equivalent to how bridge tournament deals are generated.
    print("--- 1. Deterministic Board Generation ---")
    board_1 = bigdeal.get_deal(boardno=1, owner=b"tournament-A")
    board_2 = bigdeal.get_deal(boardno=1, owner=b"tournament-A") # Should be same
    board_3 = bigdeal.get_deal(boardno=2, owner=b"tournament-A") # Should be different
    
    def print_deal_summary(hands, label):
        print(f"\n{label}:")
        for i, hand in enumerate(hands):
            # bigdeal returns list of card lists
            h = Hand(hand)
            print(f"  Seat {i}: {h}")
            
    print_deal_summary(board_1, "Board 1 (Owner A)")
    # Just check if they match (re-printed to verify)
    print_deal_summary(board_2, "Board 1 (Owner A, Repeat)")
    print_deal_summary(board_3, "Board 2 (Owner A)")
    
    # 2. Partial Deal Generation
    # Useful when some seats already have cards and you want to fill the rest
    print("\n--- 2. Partial Deal Generation ---")
    
    # Available cards (e.g., first 20 cards of the deck)
    all_cards = []
    for suit in Suit:
        for rank in sorted(list(Rank), reverse=True):
            all_cards.append(bigdeal.Card(suit, rank))
    
    available_cards = all_cards[:20]
    # We need 5 cards for each of the 4 seats
    needs = [5, 5, 5, 5]
    
    partial = bigdeal.generate_partial_deal(available_cards, needs)
    print(f"Distributed 20 cards into 4 seats of 5 cards each:")
    for i, hand in enumerate(partial):
        print(f"  Seat {i}: {Hand(hand)}")

    # 3. Mapping Algorithm
    # bigdeal uses a specific mapping between a large number (Goedel number) 
    # and a selection of k cards from n.
    print("\n--- 3. bigdeal Mapping Algorithm ---")
    cards_to_select_from = all_cards[:10] # 10 cards
    k = 3 # select 3
    # Total combinations is 10C3 = 120
    
    # Let's map number 42 to a selection
    selection, remaining = bigdeal.map_number_to_hand(42, cards_to_select_from, k)
    print(f"Selection for number 42 from 10 cards (10C3=120):")
    print(f"  Selected: {Hand(selection)}")
    print(f"  Remaining: {Hand(remaining)}")

if __name__ == "__main__":
    run_bigdeal_example()

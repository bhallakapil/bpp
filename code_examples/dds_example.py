import sys
import os

# Add parent directory to sys.path to allow importing redeal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redeal import Deal, H, Seat, Card

def run_dds_analysis():
    """
    Demonstrates dds.py functionality:
    - Solving a specific contract (tricks)
    - Solving all possible leads (lead analysis)
    - Calculating par scores/contracts
    """
    
    # 1. Setup a specific deal with known properties
    # North has a very strong hand (AKQ in all suits)
    # South has a weak hand (234 in all suits)
    predeal = {
        "N": "AKQ AKQ AKQ AKQJ",
        "S": "432 432 432 5432"
    }
    
    # Prepare the dealer and generate a deal
    # This automatically fills in the remaining cards for East/West
    dealer = Deal.prepare(predeal)
    deal = dealer()
    
    print("--- 1. Double Dummy Solver (DDS) Analysis ---")
    # Setting print style to long for better visibility
    Deal.set_str_style("long")
    print(f"Full Deal:{deal}")
    
    # 2. Solving a specific contract
    # How many tricks can North make in 7NT?
    # Expected: 13
    tricks_7nt = deal.dd_tricks("7NN")
    print(f"Tricks for 7NT by North: {tricks_7nt}")
    
    # How many tricks can North make in 7 Spades?
    tricks_7s = deal.dd_tricks("7SN")
    print(f"Tricks for 7S by North: {tricks_7s}")
    
    # 3. Solving all leads
    # If West leads against 7NT by North, what are the outcomes?
    print("\nOutcome for all possible leads by West against 7NT(N):")
    # dd_all_tricks takes (strain, leader) and returns tricks for the LEADER'S side.
    leads = deal.dd_all_tricks("N", "W")
    
    # Group results by number of tricks
    results = {}
    for card, tricks in leads.items():
        results.setdefault(tricks, []).append(card)
        
    for tricks in sorted(results.keys(), reverse=True):
        cards = ", ".join(str(c) for c in results[tricks])
        print(f"  {tricks} tricks for West (defender) if leading: {cards}")
        
    # 4. Par Score Calculation
    # Computes the optimal result if all four players play perfectly
    print("\n--- 2. Par Calculation ---")
    # par(dealer, nsvul, ewvul)
    pars = deal.par("N", nsvul=False, ewvul=False)
    
    print("Par Result (N Dealer, None Vul):")
    for p in pars:
        # ScoredContract objects have a nice __str__
        print(f"  {p}")

if __name__ == "__main__":
    try:
        run_dds_analysis()
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: DDS requires libdds.so/dds.dll to be present in the redeal/ directory.")

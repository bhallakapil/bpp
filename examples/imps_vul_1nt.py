# This simulation checks how often South gets a 4-4-3-2 hand with 8-12 HCP
# when North opens 1NT (assuming North is dealer and has passed the opening strength check).
# The hand specified: S: Jxxx, H: Jxxx, D: Axx, C: Qx implies minimum 8 HCP.

from redeal import *

# Counter for results
table = {
    "4432_8to12_HCP": 0,
    "total_deals": 0
}

# Target distribution lengths (order doesn't matter initially)
target_lengths = sorted([4, 4, 3, 2])

def accept(d):
    # 1. Check if South has a hand in the target HCP range (8-12)
    # The specified cards (J, J, A, Q) give a minimum of 8 HCP.
    south_hcp_ok = (8 <= d.south.hcp <= 12)

    # 2. Check for 4-4-3-2 distribution
    south_lengths = sorted([len(d.south.spades), len(d.south.hearts), len(d.south.diamonds), len(d.south.clubs)])
    south_shape_ok = (south_lengths == target_lengths)

    # 3. Check opponents' strength (ensuring the 1NT opening seems reasonable and opponents aren't overly strong)
    # Using similar constraints as the example, adjusted slightly.
    opponents_ok = all(opp.hcp < 16
                       and (opp.freakness < 6 and max(map(len, opp)) < 6
                            or opp.pt < 6)
                       for opp in [d.west, d.east])

    # We accept the deal if South has the desired shape/strength AND opponents are constrained.
    return south_hcp_ok and south_shape_ok and opponents_ok

def do(d):
    table["4432_8to12_HCP"] += 1
    table["total_deals"] += 1

def final(_):
    # Calculate frequency
    freq = table["4432_8to12_HCP"] / table["total_deals"] if table["total_deals"] > 0 else 0
    print(f"--- Simulation Results ---")
    print(f"Total Deals Tested: {table['total_deals']}")
    print(f"Deals with South hand matching 4-4-3-2 (8-12 HCP) vs 1NT: {table['4432_8to12_HCP']}")
    print(f"Frequency: {freq:.6f}")
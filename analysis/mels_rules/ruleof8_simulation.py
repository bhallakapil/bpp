"""
Rule of 8 Bridge Simulation & Statistical Analysis (Including Tactical Bidding Model)
----------------------------------------------------------------------------------
Simulates bridge deals matching Mel's Rule of 8 criteria:
1. South opens 1NT (15-17 HCP, balanced/semi-balanced per redeal's is_1nt library function).
2. North has any hand (no constraints).
3. West bids 2H or 2S when holding a single-suited hand in Hearts or Spades with either:
   - 5-3-3-2 shape (with 5-card major) OR
   - Single-suited shapes as per analysis/cumulative_shape_probabilities.md.
4. West has a minimum of 6 HCP.
5. West's hand satisfies the Rule of 8 / length & loser condition: (l1 + l2 - losers) >= 2.
6. East passes (unconditional/no action).
7. Evaluates Double Dummy (DD) scores for West's 2M contract versus the optimal DD par score,
   and integrates tactical auction rules (8+ card W-E major fit -> safe; North >= 9 HCP -> game).
"""

from redeal import *
from collections import Counter, defaultdict

SINGLE_SUITED_SHAPES = {
    (6, 3, 2, 2), (6, 4, 2, 1), (6, 3, 3, 1), (7, 3, 2, 1), (6, 4, 3, 0),
    (7, 2, 2, 2), (7, 4, 1, 1), (7, 4, 2, 0), (7, 3, 3, 0), (8, 2, 2, 1),
    (8, 3, 1, 1), (7, 5, 1, 0), (8, 3, 2, 0), (8, 4, 1, 0), (9, 2, 1, 1),
    (9, 3, 1, 0), (9, 2, 2, 0), (8, 5, 0, 0), (10, 2, 1, 0), (9, 4, 0, 0),
    (10, 1, 1, 1), (10, 3, 0, 0), (11, 1, 1, 0), (11, 2, 0, 0), (12, 1, 0, 0),
    (13, 0, 0, 0)
}

stats = {
    "total_deals": 0,
    "west_spades": 0,
    "west_hearts": 0,
    "total_west_score": 0,
    "par_or_better_count": 0,
    "positive_score_below_par": 0,
    "negative_score_below_par": 0,
    "fit_8_card_plus": 0,
    "north_9_hcp_plus": 0,
    "hcp_sums": {"N": 0, "E": 0, "S": 0, "W": 0},
    "loser_sums": 0,
    "l1_sums": 0,
    "controls_sums": 0,
    "west_hcp_dist": Counter(),
    "west_losers_dist": Counter(),
    "better_examples": [],
    "worse_examples": [],
}

def west_bids_major(west):
    shape = tuple(sorted(west.shape, reverse=True))
    if shape == (5, 3, 3, 2):
        if len(west.spades) == 5:
            return "S"
        if len(west.hearts) == 5:
            return "H"
    elif shape in SINGLE_SUITED_SHAPES:
        if len(west.spades) == shape[0]:
            return "S"
        if len(west.hearts) == shape[0]:
            return "H"
    return None

def accept(deal):
    if not is_1nt(deal.south):
        return False
    major = west_bids_major(deal.west)
    if major is None:
        return False
    if deal.west.hcp < 6:
        return False
    if (deal.west.l1 + deal.west.l2 - deal.west.losers) < 2:
        return False
    return True

def do(deal):
    stats["total_deals"] += 1
    
    # Track seat metrics
    for seat, hand in [("N", deal.north), ("E", deal.east), ("S", deal.south), ("W", deal.west)]:
        stats["hcp_sums"][seat] += hand.hcp
        
    stats["loser_sums"] += deal.west.losers
    stats["l1_sums"] += deal.west.l1
    stats["controls_sums"] += deal.west.controls
    
    stats["west_hcp_dist"][deal.west.hcp] += 1
    stats["west_losers_dist"][int(deal.west.losers)] += 1
    
    major = west_bids_major(deal.west)
    if major == "S":
        stats["west_spades"] += 1
    elif major == "H":
        stats["west_hearts"] += 1
        
    # Tactical model checks
    east_support = len(deal.east.spades if major == "S" else deal.east.hearts) >= 3
    north_strong = deal.north.hcp >= 9
    if east_support:
        stats["fit_8_card_plus"] += 1
    if north_strong:
        stats["north_9_hcp_plus"] += 1
        
    west_score = deal.dd_score(f"2{major}W", vul=False)
    stats["total_west_score"] += west_score
    
    pars = deal.par("N", nsvul=False, ewvul=False)
    ns_par = pars[0].score
    ew_par = -ns_par
    
    is_better_or_equal = west_score >= ew_par
    if is_better_or_equal:
        stats["par_or_better_count"] += 1
        if len(stats["better_examples"]) < 3:
            stats["better_examples"].append((deal, major, west_score, ew_par, pars[0]))
    else:
        if west_score > 0:
            stats["positive_score_below_par"] += 1
        else:
            stats["negative_score_below_par"] += 1
        if len(stats["worse_examples"]) < 3:
            stats["worse_examples"].append((deal, major, west_score, ew_par, pars[0]))

def format_hand(h):
    return f"S: {str(h.spades):<15} H: {str(h.hearts):<15} D: {str(h.diamonds):<15} C: {str(h.clubs):<15}"

def final(n_tries):
    c = stats["total_deals"]
    print(f"--- RULE OF 8 SIMULATION RESULTS & TACTICAL MODEL ---")
    print(f"Total iterations attempted: {n_tries}")
    print(f"Total matching deals accepted: {c}")
    if c > 0:
        print(f"\n[Bidding & Performance]")
        print(f"West bids Spades: {stats['west_spades']} ({stats['west_spades']/c*100:.2f}%)")
        print(f"West bids Hearts: {stats['west_hearts']} ({stats['west_hearts']/c*100:.2f}%)")
        avg_west_score = stats["total_west_score"] / c
        pct_par_or_better = (stats["par_or_better_count"] / c) * 100
        pct_positive_below_par = (stats["positive_score_below_par"] / c) * 100
        pct_negative_below_par = (stats["negative_score_below_par"] / c) * 100
        print(f"Average DD Score for West's 2M contract: {avg_west_score:.2f}")
        print(f"Percentage achieving Par score or better for EW: {pct_par_or_better:.2f}%")
        print(f"Percentage below par with Positive West Score (Disruptive Gain): {pct_positive_below_par:.2f}%")
        print(f"Percentage below par with Negative West Score (Penalty Loss): {pct_negative_below_par:.2f}%")
        
        print(f"\n[Tactical Model Assumptions]")
        pct_fit = (stats["fit_8_card_plus"] / c) * 100
        pct_north_game = (stats["north_9_hcp_plus"] / c) * 100
        print(f"W-E 8+ Card Major Fit (East >= 3 card support): {stats['fit_8_card_plus']} ({pct_fit:.2f}%)")
        print(f"North >= 9 HCP (North bids game or higher): {stats['north_9_hcp_plus']} ({pct_north_game:.2f}%)")
        
        print(f"\n[Average HCP per Seat]")
        for seat in ["N", "E", "S", "W"]:
            print(f"  Seat {seat}: {stats['hcp_sums'][seat] / c:.2f} HCP")
            
        print(f"\n[West Hand Characteristics]")
        print(f"  Average Loser Trick Count (LTC): {stats['loser_sums'] / c:.2f}")
        print(f"  Average Longest Suit Length (l1): {stats['l1_sums'] / c:.2f}")
        print(f"  Average Controls (A=2, K=1): {stats['controls_sums'] / c:.2f}")
        
        print(f"\n[West HCP Distribution]")
        for hcp_val in sorted(stats["west_hcp_dist"].keys()):
            cnt = stats["west_hcp_dist"][hcp_val]
            print(f"  {hcp_val} HCP: {cnt} ({cnt/c*100:.2f}%)")
            
        print(f"\n[West Loser Count Distribution]")
        for l_val in sorted(stats["west_losers_dist"].keys()):
            cnt = stats["west_losers_dist"][l_val]
            print(f"  {l_val} Losers: {cnt} ({cnt/c*100:.2f}%)")
            
        print("\n--- Better/Equal Par Examples ---")
        for i, (deal, m, w_score, e_par, par_contract) in enumerate(stats["better_examples"], 1):
            print(f"{i}. West 2{m} Score: {w_score}, EW Par: {e_par} (Par Contract: {par_contract})")
            print(f"  North: {format_hand(deal.north)}")
            print(f"  West:  {format_hand(deal.west)}")
            print(f"  East:  {format_hand(deal.east)}")
            print(f"  South: {format_hand(deal.south)}")
            print("-" * 60)
            
        print("\n--- Worse than Par Examples ---")
        for i, (deal, m, w_score, e_par, par_contract) in enumerate(stats["worse_examples"], 1):
            print(f"{i}. West 2{m} Score: {w_score}, EW Par: {e_par} (Par Contract: {par_contract})")
            print(f"  North: {format_hand(deal.north)}")
            print(f"  West:  {format_hand(deal.west)}")
            print(f"  East:  {format_hand(deal.east)}")
            print(f"  South: {format_hand(deal.south)}")
            print("-" * 60)
    else:
        print("No matching deals found.")

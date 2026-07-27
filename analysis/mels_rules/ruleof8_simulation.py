"""
Rule of 8 Bridge Simulation & Statistical Analysis (Unified Script with Caching)
-------------------------------------------------------------------------------
Simulates or loads 100,000 bridge deals matching Mel's Rule of 8 criteria:
1. South opens 1NT (15-17 HCP, balanced/semi-balanced per redeal's is_1nt library function).
2. North has any hand (no constraints).
3. West bids 2H or 2S when holding a single-suited hand in Hearts or Spades with either:
   - 5-3-3-2 shape (with 5-card major) OR
   - Single-suited shapes as per analysis/cumulative_shape_probabilities.md.
4. West has a minimum of 6 HCP.
5. West's hand satisfies the Rule of 8 / length & loser condition: (l1 + l2 - losers) >= 2.
6. East passes (unconditional/no action).
7. Evaluates Double Dummy (DD) scores for West's 2M contract versus the optimal DD par score.
"""

import os
import sys
import time
from redeal import is_1nt, Hand, Deal, Seat
from collections import Counter, defaultdict

SINGLE_SUITED_SHAPES = {
    (6, 3, 2, 2), (6, 4, 2, 1), (6, 3, 3, 1), (7, 3, 2, 1), (6, 4, 3, 0),
    (7, 2, 2, 2), (7, 4, 1, 1), (7, 4, 2, 0), (7, 3, 3, 0), (8, 2, 2, 1),
    (8, 3, 1, 1), (7, 5, 1, 0), (8, 3, 2, 0), (8, 4, 1, 0), (9, 2, 1, 1),
    (9, 3, 1, 0), (9, 2, 2, 0), (8, 5, 0, 0), (10, 2, 1, 0), (9, 4, 0, 0),
    (10, 1, 1, 1), (10, 3, 0, 0), (11, 1, 1, 0), (11, 2, 0, 0), (12, 1, 0, 0),
    (13, 0, 0, 0)
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

def parse_pbn_line(line):
    inner = line.split('"')[1]
    _, hands_str = inner.split(":")
    hands = [Hand.from_str(h.replace('.', ' ')) for h in hands_str.split()]
    return Deal(dict(zip(Seat, hands)))

def get_or_generate_deals(target=1000):
    os.makedirs("cached-dir", exist_ok=True)
    cache_path = "cached-dir/ruleof8_deals_1000.pbn"
    
    deals = []
    if os.path.exists(cache_path):
        print(f"Loading cached deals from {cache_path}...")
        start_time = time.time()
        with open(cache_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    deals.append(parse_pbn_line(line))
                if len(deals) >= target:
                    break
        print(f"Loaded {len(deals)} deals in {time.time() - start_time:.2f} seconds.")
        if len(deals) >= target:
            return deals

    print(f"Generating {target} accepted deals via redeal...")
    start_time = time.time()
    boardno = 0
    Deal.set_str_style("pbn")
    generate_deal = Deal.prepare()
    
    with open(cache_path, "w") as f:
        while len(deals) < target:
            deal = generate_deal()
            boardno += 1
            if accept(deal):
                pbn_str = deal._pbn_str()
                f.write(pbn_str + "\n")
                deals.append(deal)
                if len(deals) % 1000 == 0:
                    elapsed = time.time() - start_time
                    rate = len(deals) / elapsed if elapsed > 0 else 0
                    pct = (len(deals) / boardno) * 100
                    print(f"Caching progress: {len(deals)}/{target} deals (Tries: {boardno}, Acceptance Rate: {pct:.3f}%, Speed: {rate:.1f} deals/sec)...")
                    
    total_time = time.time() - start_time
    file_size_mb = os.path.getsize(cache_path) / (1024 * 1024)
    final_acceptance_pct = (target / boardno) * 100
    print(f"\nCache complete! Stored {target} deals in {cache_path}")
    print(f"Total iterations attempted: {boardno}")
    print(f"Match criteria acceptance rate: {final_acceptance_pct:.3f}%")
    print(f"File size: {file_size_mb:.2f} MB")
    return deals

def format_hand(h):
    return f"S: {str(h.spades):<15} H: {str(h.hearts):<15} D: {str(h.diamonds):<15} C: {str(h.clubs):<15}"

def run_simulation():
    deals = get_or_generate_deals(100000)
    
    stats = {
        "total_deals": 0,
        "west_spades": 0,
        "west_hearts": 0,
        "total_west_score": 0,
        "par_or_better_count": 0,
        "hcp_sums": {"N": 0, "E": 0, "S": 0, "W": 0},
        "loser_sums": 0,
        "l1_sums": 0,
        "controls_sums": 0,
        "west_hcp_dist": Counter(),
        "west_losers_dist": Counter(),
        "better_examples": [],
        "worse_examples": [],
    }
    
    print(f"\nAnalyzing {len(deals)} cached deals...")
    start_time = time.time()
    
    for deal in deals:
        stats["total_deals"] += 1
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
            if len(stats["worse_examples"]) < 3:
                stats["worse_examples"].append((deal, major, west_score, ew_par, pars[0]))
                
    print(f"Analysis completed in {time.time() - start_time:.2f} seconds.\n")
    
    # Print final results
    c = stats["total_deals"]
    print(f"--- RULE OF 8 SIMULATION RESULTS & DETAILED STATS (100k Cached Deals) ---")
    print(f"Total matching deals analyzed: {c}")
    if c > 0:
        print(f"\n[Bidding & Performance]")
        print(f"West bids Spades: {stats['west_spades']} ({stats['west_spades']/c*100:.2f}%)")
        print(f"West bids Hearts: {stats['west_hearts']} ({stats['west_hearts']/c*100:.2f}%)")
        avg_west_score = stats["total_west_score"] / c
        pct_par_or_better = (stats["par_or_better_count"] / c) * 100
        print(f"Average DD Score for West's 2M contract: {avg_west_score:.2f}")
        print(f"Percentage achieving Par score or better for EW: {pct_par_or_better:.2f}%")
        
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

if __name__ == "__main__":
    run_simulation()

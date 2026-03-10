from redeal import *

# South hand: 7542 J975 K97 KQ
predeal = {"S": "7542 J975 K97 KQ"}

def accept(deal):
    n = deal.north
    # North opens 1NT: 15-17 HCP, Balanced
    if not (15 <= n.hcp <= 17):
        return False
    if not balanced(n):
        return False
    # To evaluate 4S/4H vs 3NT, we check for 4-4 fits.
    return len(n.spades) >= 4 or len(n.hearts) >= 4

stats = {"3N_Makes": 0, "4S_Makes": 0, "4H_Makes": 0, "count_S": 0, "count_H": 0, "count_total": 0}

def do(deal):
    stats["count_total"] += 1
    n = deal.north
    
    # 3NT is always an option
    makes_3n = deal.dd_tricks("3NN") >= 9
    if makes_3n:
        stats["3N_Makes"] += 1

    # Check Spades fit
    if len(n.spades) >= 4:
        stats["count_S"] += 1
        if deal.dd_tricks("4SN") >= 10:
            stats["4S_Makes"] += 1
            
    # Check Hearts fit
    if len(n.hearts) >= 4:
        stats["count_H"] += 1
        if deal.dd_tricks("4HN") >= 10:
            stats["4H_Makes"] += 1

def final(n_tries):
    c = stats["count_total"]
    if c > 0:
        print(f"--- SIMULATION RESULTS (Success Rates) ---")
        print(f"South Hand: 7542 J975 K97 KQ (9 HCP, 4-4-3-2)")
        print(f"Against 1NT opener (15-17 HCP, Balanced)")
        print(f"Total deals: {c}")
        
        rate_3nt = 100 * stats['3N_Makes'] / c
        print(f"3NT makes: {stats['3N_Makes']} times ({rate_3nt:.1f}%)")
        
        if stats["count_S"] > 0:
            rate_4s = 100 * stats['4S_Makes'] / stats["count_S"]
            print(f"4S makes (when 4-4 fit): {stats['4S_Makes']}/{stats['count_S']} ({rate_4s:.1f}%)")
            
        if stats["count_H"] > 0:
            rate_4h = 100 * stats['4H_Makes'] / stats["count_H"]
            print(f"4H makes (when 4-4 fit): {stats['4H_Makes']}/{stats['count_H']} ({rate_4h:.1f}%)")
    else:
        print("No deals matched the constraints.")

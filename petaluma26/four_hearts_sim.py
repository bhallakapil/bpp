from redeal import *

# South hand: S A76 H KT9543 D AJ7 C 6
predeal = {"S": "A76 KT9543 AJ7 6"}

import random

stats = {
    7: {"3h": 0, "4h": 0, "count": 0},
    8: {"3h": 0, "4h": 0, "count": 0},
    9: {"3h": 0, "4h": 0, "count": 0},
}

def accept(deal):
    w = deal.west
    n = deal.north
    
    # West: 11-15 HCP, <= 2 Hearts
    if not (11 <= w.hcp <= 15):
        return False
    if len(w.hearts) > 2:
        return False

    # West Shapes: 4243 4234 4144 4153 4135 4054 4045
    # Also 3253, 3235, 3154, 3145
    allowed_shapes = [
        (4, 2, 4, 3), (4, 2, 3, 4), (4, 1, 4, 4), 
        (4, 1, 5, 3), (4, 1, 3, 5), (4, 0, 5, 4), (4, 0, 4, 5),
        (3, 2, 5, 3), (3, 2, 3, 5), (3, 1, 5, 4), (3, 1, 4, 5)
    ]
    if w.shape not in allowed_shapes:
        return False
        
    # North: exactly 3 Hearts, 7-9 HCP
    if len(n.hearts) != 3:
        return False
    if not (7 <= n.hcp <= 9):
        return False
        
    return True

def do(deal):
    n_hcp = deal.north.hcp
    tricks = deal.dd_tricks("4HS")
    
    stats[n_hcp]["count"] += 1
    if tricks >= 9:
        stats[n_hcp]["3h"] += 1
    if tricks >= 10:
        stats[n_hcp]["4h"] += 1

def final(n_tries):
    print(f"{'North HCP':<10} | {'3H Success %':<15} | {'4H Success %':<15} | {'Count':<6}")
    print("-" * 55)
    
    strategy_successes = 0
    strategy_total = 0
    
    for hcp in [7, 8, 9]:
        d = stats[hcp]
        c = d["count"]
        if c > 0:
            p3 = 100 * d["3h"] / c
            p4 = 100 * d["4h"] / c
            print(f"{hcp:<10} | {p3:>13.1f}% | {p4:>13.1f}% | {c:<6}")
            
            # Strategy:
            # 7 HCP: 100% 3H
            # 8 HCP: 50% 3H, 50% 4H
            # 9 HCP: 100% 4H
            if hcp == 7:
                strategy_successes += d["3h"]
                strategy_total += c
            elif hcp == 8:
                # We simulate 50/50 split of the total count for this HCP
                # To be precise, we use the actual successes
                # (Expected success rate for HCP 8 Strategy)
                strategy_successes += 0.5 * d["3h"] + 0.5 * d["4h"]
                strategy_total += c
            elif hcp == 9:
                strategy_successes += d["4h"]
                strategy_total += c
                
    if strategy_total > 0:
        print("-" * 55)
        print(f"Overall Strategy Success Rate: {100 * strategy_successes / strategy_total:.1f}%")


if __name__ == "__main__":
    dealer = Deal.prepare(predeal)
    # Use 5000 successful trials
    count = 0
    while count < 5000:
        try:
            # We increase tries per attempt to find valid deals
            deal = dealer(accept_func=accept, tries=20000)
            do(deal)
            count += 1
        except Exception as e:
            print(f"Stopped after {count} trials: {e}")
            break
    final(count)

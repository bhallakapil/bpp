from redeal import *

# South hand: 8 5 H K 3 2 D K 7 6 2 C Q J 3 2
predeal = {"S": "85 K32 K762 QJ32"}

stats = {
    15: {"1N": 0, "2N": 0, "3N": 0, "count": 0},
    16: {"1N": 0, "2N": 0, "3N": 0, "count": 0},
    17: {"1N": 0, "2N": 0, "3N": 0, "count": 0}
}

def accept(deal):
    n = deal.north
    # 15-17 HCP
    if not (15 <= n.hcp <= 17):
        return False
    
    # Shape: Balanced or Semi-balanced with 6-card minor, no 5-4 majors
    s, h, d, c = n.shape
    # is_balanced includes 4333, 4432, 5332 in redeal
    is_balanced = n.shape in balanced
    is_6_minor_semi = (sorted(n.shape) == [2, 2, 3, 6] and (d == 6 or c == 6))
    if not (is_balanced or is_6_minor_semi):
        return False
    if (s == 5 and h == 4) or (s == 4 and h == 5):
        return False
    if s >= 6 or h >= 6:
        return False
        
    return True

def do(deal):
    n = deal.north
    hcp = n.hcp
    stats[hcp]["count"] += 1
    
    # Max tricks in NT with North as declarer (1NT opener)
    tricks = deal.dd_tricks("1NN")
    
    if tricks >= 7:
        stats[hcp]["1N"] += 1
    if tricks >= 8:
        stats[hcp]["2N"] += 1
    if tricks >= 9:
        stats[hcp]["3N"] += 1

def final(n_tries):
    print(f"{'HCP':<5} | {'1N %':<8} | {'2N %':<8} | {'3N %':<8} | {'Count':<6}")
    print("-" * 45)
    
    total_1n = 0
    total_3n = 0
    total_count = 0
    
    for hcp in [15, 16, 17]:
        d = stats[hcp]
        c = d["count"]
        if c > 0:
            p1 = 100 * d["1N"] / c
            p2 = 100 * d["2N"] / c
            p3 = 100 * d["3N"] / c
            print(f"{hcp:<5} | {p1:>7.1f}% | {p2:>7.1f}% | {p3:>7.1f}% | {c:<6}")
            total_1n += d["1N"]
            total_3n += d["3N"]
            total_count += c
            
    if total_count > 0:
        print("-" * 45)
        print(f"{'Total':<5} | {100*total_1n/total_count:>7.1f}% | {'-':>8} | {100*total_3n/total_count:>7.1f}% | {total_count:<6}")
        
    # Additional: 2N success rate if partner has 15-16 HCP
    count_1516 = stats[15]["count"] + stats[16]["count"]
    if count_1516 > 0:
        succ_1516_2n = (stats[15]["2N"] + stats[16]["2N"]) / count_1516 * 100
        print(f"\n2N success rate (North 15-16 HCP): {succ_1516_2n:.1f}%")

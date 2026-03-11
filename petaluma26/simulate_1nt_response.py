from redeal import *

# South hand: 8 5 H K 3 2 D K 7 6 2 C Q J 3 2
predeal = {"S": "85 K32 K762 QJ32"}

stats = {
    15: {"1N": 0, "2N": 0, "3N": 0, "count": 0},
    16: {"1N": 0, "2N": 0, "3N": 0, "count": 0},
    17: {"1N": 0, "2N": 0, "3N": 0, "count": 0}
}

def accept(deal):
    return is_1nt(deal.north)

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

from redeal import *

# S: AQ3 H KJT83 D T6 C AQ2
predeal = {"S": "AQ3 KJT83 T6 AQ2"}

def accept(deal):
    n = deal.north
    # 0-6 HCP and no length constraint on hearts
    return (0 <= n.hcp <= 6)

stats = {"1N": 0, "2H": 0, "count": 0}

def do(deal):
    stats["count"] += 1
    # Check 1N (7 tricks)
    if deal.dd_tricks("1NNS") >= 7:
        stats["1N"] += 1
        
    # Check 2H (8 tricks)
    if deal.dd_tricks("2HS") >= 8:
        stats["2H"] += 1

def final(n_tries):
    c = stats["count"]
    if c > 0:
        print(f"FINAL SUMMARY")
        print(f"Out of {c} deals:")
        n1_rate = 100 * stats['1N'] / c
        h2_rate = 100 * stats['2H'] / c
        print(f"1N makes {stats['1N']} times ({n1_rate:.1f}%)")
        print(f"2H makes {stats['2H']} times ({h2_rate:.1f}%)")
        if stats['2H'] > stats['1N']:
            print("Conclusion: 2H is better to bid.")
        elif stats['1N'] > stats['2H']:
            print("Conclusion: 1N is better to bid.")
        else:
            print("Conclusion: Both contracts have equal make rates.")
    else:
        print("No deals matched the constraints.")

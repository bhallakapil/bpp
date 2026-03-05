from redeal import *

# S: AQ3 H KJT83 D T6 C AQ2
predeal = {"S": "AQ3 KJT83 T6 AQ2"}

def accept(deal):
    n = deal.north
    return (8 <= n.hcp <= 10 and len(n.hearts) == 3)

stats = {"3N": 0, "4H": 0, "count": 0}

def do(deal):
    stats["count"] += 1
    # Check 3N
    if deal.dd_tricks("3NNS") >= 9:
        stats["3N"] += 1
        
    # Check 4H
    if deal.dd_tricks("4HS") >= 10:
        stats["4H"] += 1

def final(n_tries):
    c = stats["count"]
    if c > 0:
        print(f"FINAL SUMMARY")
        print(f"Out of {c} deals:")
        n3_rate = 100 * stats['3N'] / c
        h4_rate = 100 * stats['4H'] / c
        print(f"3N makes {stats['3N']} times ({n3_rate:.1f}%)")
        print(f"4H makes {stats['4H']} times ({h4_rate:.1f}%)")
        if stats['4H'] > stats['3N']:
            print("Conclusion: 4H is better to bid.")
        elif stats['3N'] > stats['4H']:
            print("Conclusion: 3N is better to bid.")
        else:
            print("Conclusion: Both contracts have equal make rates.")
    else:
        print("No deals matched the constraints.")

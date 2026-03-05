from redeal import *

predeal = {"S": "KQ9 A643 A54 J32"}

def accept(deal):
    n, e, w = deal.north, deal.east, deal.west
    return (n.hcp >= 11 and n.hcp <= 14 and len(n.clubs) >= 3 and
            e.hcp < 12 and
            8 <= w.hcp <= 15 and len(w.spades) >= 5 and
            len(n.hearts) == 4 and
            len(e.spades) >= 3 and e.hcp >= 5 and
            A in e.clubs and
            A in w.spades)

stats = {"3N": 0, "4H": 0, "count": 0}

def do(deal):
    stats["count"] += 1
    if deal.dd_tricks("3NS") >= 9:
        stats["3N"] += 1
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

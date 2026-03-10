from redeal import *
import statistics
import sys

# South's hand: S AJ10953 H J1073 D 103 C 4
predeal = {"S": "AJT953 JT73 T3 4"}

# The final contract is 3N by East (3NE)
FINAL_CONTRACT = "3NE"

def accept(deal):
    east = deal.east
    west = deal.west
    
    # East HCP: 20-21
    if not (20 <= east.hcp <= 21):
        return False
        
    # East Shape: Balanced or Semi-balanced with 6-card minor, no 5-4 majors, plus 2245 and 2254
    s, h, d, c = east.shape
    is_balanced = east.shape in balanced
    is_6_minor_semi = (sorted(east.shape) == [2, 2, 3, 6] and (d == 6 or c == 6))
    is_2245 = (s == 2 and h == 2 and d == 4 and c == 5)
    is_2254 = (s == 2 and h == 2 and d == 5 and c == 4)
    
    if not (is_balanced or is_6_minor_semi or is_2245 or is_2254):
        return False
        
    if (s == 5 and h == 4) or (s == 4 and h == 5):
        return False
        
    # West: 3-12 HCP
    if not (3 <= west.hcp <= 12):
        return False
        
    # West: can have 4333 or 3433 hand, or <=3 in majors
    sw, hw, dw, cw = west.shape
    if (sw > 3 or hw > 3) and not (west.shape == (4,3,3,3) or west.shape == (3,4,3,3)):
        return False

    # West: no voids, no suit > 6, two longest suits <= 9
    if 0 in west.shape or max(west.shape) > 6 or sum(sorted(west.shape)[2:]) > 9:
        return False
        
    return True

class OpeningLeadAnalysis(Simulation):
    def __init__(self):
        self.comparisons = {
            "H3": {"more": 0, "same": 0, "less": 0},
            "DT": {"more": 0, "same": 0, "less": 0},
            "C4": {"more": 0, "same": 0, "less": 0}
        }
        self.count = 0

    def do(self, deal):
        all_leads_data = deal.dd_all_tricks("N", "S")
        
        sj = Card(Suit.S, Rank["J"])
        h3 = Card(Suit.H, Rank["3"])
        dt = Card(Suit.D, Rank["T"])
        c4 = Card(Suit.C, Rank["4"])
        
        if sj not in all_leads_data:
            return
            
        tricks_sj = 13 - all_leads_data[sj]
        
        for other, label in [(h3, "H3"), (dt, "DT"), (c4, "C4")]:
            if other in all_leads_data:
                tricks_other = 13 - all_leads_data[other]
                if tricks_sj > tricks_other:
                    self.comparisons[label]["more"] += 1
                elif tricks_sj == tricks_other:
                    self.comparisons[label]["same"] += 1
                else:
                    self.comparisons[label]["less"] += 1
        
        self.count += 1
        if self.count % 100 == 0:
            print(f"Progress: {self.count}/10000 samples completed", file=sys.stderr)

    def final(self, n_tries):
        print(f"\n### Lead Analysis: SJ vs Others (Total Samples: {self.count})")
        print("| Lead | SJ More | SJ Same | SJ Less |")
        print("| :--- | :---: | :---: | :---: |")
        for label in ["H3", "DT", "C4"]:
            res = self.comparisons[label]
            print(f"| {label} | {res['more']} | {res['same']} | {res['less']} |")

if __name__ == "__main__":
    dealer = Deal.prepare(predeal)
    sim = OpeningLeadAnalysis()
    count = 0
    while count < 10000:
        try:
            # Increase tries to 1,000,000 to be more resilient
            deal = dealer(accept_func=accept, tries=1000000)
            sim.do(deal)
            count += 1
        except Exception as e:
            # If it still fails, just log and keep going
            print(f"Warning: {e}", file=sys.stderr)
            continue
    sim.final(count)

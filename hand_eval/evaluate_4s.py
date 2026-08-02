import sys
import os
from collections import defaultdict, Counter

# Add project root to sys.path
sys.path.append(os.getcwd())

from redeal import *

predeal = {"S": "AQ853 T82 A AQ52"}

def accept(deal):
    n = deal.north
    # 1. N HCP range is 5-9
    if not (5 <= n.hcp <= 9):
        return False
    # 2. Minimal 3 spades
    if len(n.spades) < 3:
        return False
        
    side_suits = [n.hearts, n.diamonds, n.clubs]
    has_singleton = any(len(suit) == 1 for suit in side_suits)
    
    # 3. 3-card spade singleton OK, but 4+ spade singleton excluded
    if len(n.spades) >= 4 and has_singleton:
        return False
            
    return True

def simulate():
    dealer = Deal.prepare(predeal)
    n_samples = 10000
    total = 0
    
    matrices = {
        3: defaultdict(lambda: {True: {"total": 0, "makes": 0}, False: {"total": 0, "makes": 0}}),
        4: defaultdict(lambda: {True: {"total": 0, "makes": 0}, False: {"total": 0, "makes": 0}}),
        5: defaultdict(lambda: {True: {"total": 0, "makes": 0}, False: {"total": 0, "makes": 0}}) # 5+ spades
    }
    
    spade_counts = Counter()
    total_makes = 0
    
    print(f"Simulating {n_samples} hands with updates every 1,000 hands...")
    for i in range(n_samples):
        deal = dealer(accept_func=accept)
        total += 1
        n = deal.north
        spade_len = len(n.spades)
        
        if spade_len >= 5:
            spade_cat = 5
            spade_counts["5+"] += 1
        else:
            spade_cat = spade_len
            spade_counts[str(spade_len)] += 1
            
        side_suits = [n.hearts, n.diamonds, n.clubs]
        has_singleton = any(len(suit) == 1 for suit in side_suits)
        
        makes_4s = deal.dd_tricks("4SN") >= 10
        
        matrices[spade_cat][n.hcp][has_singleton]["total"] += 1
        if makes_4s:
            matrices[spade_cat][n.hcp][has_singleton]["makes"] += 1
            total_makes += 1
            
        if (i + 1) % 1000 == 0:
            print(f"Processed {i + 1}/{n_samples} hands... (Current makes: {total_makes}/{total} = {100*total_makes/total:.2f}%)")
            
    print(f"\n# Simulation Results for 4S ({n_samples} hands)\n")
    print(f"**Overall 4S makes:** {total_makes}/{total} (**{100 * total_makes / total:.2f}%**)\n")
    
    print("## North Spade Length Percentages\n")
    for k in sorted(spade_counts.keys()):
        pct = 100 * spade_counts[k] / total
        print(f"- **{k} Spades:** {spade_counts[k]}/{total} ({pct:.2f}%)")
    print()
    
    for spade_len in [3, 4, 5]:
        title_len = "5+ Spades" if spade_len == 5 else f"{spade_len} Spades"
        print(f"## Matrix for {title_len} Holding: HCP vs Singleton Status\n")
        print("| HCP | With Singleton (Makes / Total, %) | Without Singleton (Makes / Total, %) |")
        print("| :--- | :--- | :--- |")
        
        mat = matrices[spade_len]
        for hcp in sorted(mat.keys()):
            ws = mat[hcp][True]
            wos = mat[hcp][False]
            
            ws_str = f"{ws['makes']}/{ws['total']} ({100*ws['makes']/ws['total']:.1f}%)" if ws['total'] > 0 else "0/0 (0.0%)"
            wos_str = f"{wos['makes']}/{wos['total']} ({100*wos['makes']/wos['total']:.1f}%)" if wos['total'] > 0 else "0/0 (0.0%)"
            
            print(f"| {hcp} | {ws_str} | {wos_str} |")
        print()

if __name__ == "__main__":
    simulate()

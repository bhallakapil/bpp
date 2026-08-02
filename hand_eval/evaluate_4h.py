import sys
import os
from collections import defaultdict, Counter

# Add project root to sys.path
sys.path.append(os.getcwd())

from redeal import *

predeal = {"S": "KQJ AKJ975 JT3 4"}

shape_4333 = Shape("(4333)")

def accept(deal):
    n = deal.north
    e = deal.east
    w = deal.west
    
    # 1. N HCP range 7-9
    if not (7 <= n.hcp <= 9):
        return False
    # 2. N has 3+ hearts
    if len(n.hearts) < 3:
        return False
    # 3. N has 4333 shape
    if not shape_4333(n):
        return False
    # 4. E & W have equal points
    if e.hcp != w.hcp:
        return False
        
    return True

def simulate():
    dealer = Deal.prepare(predeal)
    n_samples = 10000
    total = 0
    makes = 0
    
    hcp_stats = defaultdict(lambda: {"total": 0, "makes": 0})
    heart_counts = Counter()
    
    print(f"Simulating {n_samples} hands for 4H evaluation (7-9 HCP)...")
    for i in range(n_samples):
        try:
            deal = dealer(accept_func=accept, tries=30000)
        except Exception:
            continue
        total += 1
        n = deal.north
        hcp = n.hcp
        h_len = len(n.hearts)
        
        heart_counts[h_len] += 1
        hcp_stats[hcp]["total"] += 1
        
        makes_4h = deal.dd_tricks("4HN") >= 10 or deal.dd_tricks("4HS") >= 10
        if makes_4h:
            makes += 1
            hcp_stats[hcp]["makes"] += 1
            
        if (i + 1) % 2000 == 0:
            print(f"Processed {i + 1}/{n_samples} hands...", file=sys.stderr)
            
    print(f"\n# Simulation Results for 4H ({total} hands)\n")
    print(f"**Overall 4H makes:** {makes}/{total} (**{100 * makes / total:.2f}%**)\n")
    
    print("## North Heart Length Percentages\n")
    for k in sorted(heart_counts.keys()):
        pct = 100 * heart_counts[k] / total
        print(f"- **{k} Hearts:** {heart_counts[k]}/{total} ({pct:.2f}%)")
    print()
    
    print("## Breakdown by North HCP\n")
    print("| HCP | Makes / Total, % |")
    print("| :--- | :--- |")
    for hcp in sorted(hcp_stats.keys()):
        st = hcp_stats[hcp]
        t = st["total"]
        m = st["makes"]
        pct = 100 * m / t if t > 0 else 0
        print(f"| {hcp} | {m}/{t} ({pct:.1f}%) |")

if __name__ == "__main__":
    simulate()

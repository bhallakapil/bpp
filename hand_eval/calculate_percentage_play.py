import sys
import os

# Add project root to sys.path
sys.path.append(os.getcwd())

from redeal import *

def simulate():
    # North: ♠K, ♥432, ♦AKJT43, ♣AQJ
    # South: ♠AQT98765, ♥A, ♦2, ♣543
    predeal = {
        "N": "K 432 AKJT43 AQJ",
        "S": "AQT98765 A 2 543"
    }
    
    dealer = Deal.prepare(predeal)
    n_samples = 1000000 # 1 million
    
    stats = {
        "opt1": 0,
        "opt2": 0,
        "opt3": 0,
        "opt4": 0,
        "opt5": 0,
        "opt6": 0,
        "total": 0
    }
    
    print(f"Simulating {n_samples} hands for 7S (All 6 Options)...")
    
    for _ in range(n_samples):
        deal = dealer()
        stats["total"] += 1
        
        # Spade split (Opponents have J, 4, 3, 2)
        s_west = deal.west.spades
        s_east = deal.east.spades
        s_split_west = len(s_west)
        s_split_east = len(s_east)
        
        # 7S fails on 4-0 trump splits
        if s_split_west == 0 or s_split_east == 0: continue
        
        sj_singleton = (s_split_west == 1 and J in s_west) or (s_split_east == 1 and J in s_east)
        west_has_ck = K in deal.west.clubs
        west_has_dq = Q in deal.west.diamonds
        east_has_dq = Q in deal.east.diamonds
        d_west_count = len(deal.west.diamonds)
        d_east_count = len(deal.east.diamonds)
        d_split = sorted([d_west_count, d_east_count])
        
        # 1. Option 1: Club Finesse
        if west_has_ck or sj_singleton: stats["opt1"] += 1
        
        # 2. Option 2: Diamond Finesse
        if west_has_dq or sj_singleton: stats["opt2"] += 1
                
        # 3. Option 3: DA + 1 ruff
        opt3_works = sj_singleton or (d_split == [3, 3]) or (d_west_count <= 2 and west_has_dq) or (d_east_count <= 2 and east_has_dq)
        if opt3_works: stats["opt3"] += 1
            
        # 4. Option 4: Two ruffs
        overruff_safe = not (d_west_count == 2 and J in s_west and not west_has_dq)
        opt4_works = sj_singleton
        if not opt4_works:
            if d_split in [[3, 3], [2, 4]]:
                if overruff_safe: opt4_works = True
            elif d_split == [1, 5]:
                if (d_west_count == 1 and west_has_dq) or (d_east_count == 1 and east_has_dq):
                    opt4_works = True
        if opt4_works: stats["opt4"] += 1

        # 5. Option 5: Try establishment via 1 ruff (Option 3 style), then Club Finesse backup.
        # Works if Option 3 works OR Club finesse wins.
        if opt3_works or west_has_ck:
            stats["opt5"] += 1
            
        # 6. Option 6: Try establishment via 2 ruffs (Option 4 style), then Club Finesse backup.
        # Safe from overruffs: only West can overruff South.
        overruff_on_r1 = (d_west_count == 1 and J in s_west and not west_has_dq)
        overruff_on_r2 = (d_west_count == 2 and J in s_west and not west_has_dq)
        
        if sj_singleton:
            stats["opt6"] += 1
        elif not overruff_on_r1 and not overruff_on_r2:
            # Safe to attempt ruffing. Success if it establishes OR if Club finesse works.
            established = (d_split in [[3, 3], [2, 4]]) or \
                         (d_split == [1, 5] and ((d_west_count == 1 and west_has_dq) or (d_east_count == 1 and east_has_dq)))
            if established or west_has_ck:
                stats["opt6"] += 1
            
    c = stats["total"]
    print(f"Final Results for 7S from {c} total hands (1M):")
    print(f"Option 1 (Club finesse): {100*stats['opt1']/c:.3f}%")
    print(f"Option 2 (Diamond finesse): {100*stats['opt2']/c:.3f}%")
    print(f"Option 3 (DA + 1 ruff): {100*stats['opt3']/c:.3f}%")
    print(f"Option 4 (Two ruffs): {100*stats['opt4']/c:.3f}%")
    print(f"Option 5 (Opt 3 + C finesse backup): {100*stats['opt5']/c:.3f}%")
    print(f"Option 6 (Opt 4 + C finesse backup): {100*stats['opt6']/c:.3f}%")

if __name__ == "__main__":
    simulate()

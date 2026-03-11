from collections import Counter
from redeal import *

# South hand: J9875 K5 Q873 KJ (10 HCP, 5-2-4-2)
predeal = {"S": "J9875 K5 Q873 KJ"}

def initial():
    global TABLE_IMPS, TABLE_MP
    # Compare 4 strategies for a 5-card major hand:
    # 0: Pass 1NT (Conservative)
    # 1: Bid 3NT (Fast arrival, hide spades)
    # 2: Transfer to Game (Choice of 4S/3NT)
    # 3: Transfer Invite (Choice of 4S/3S/3NT/2NT)
    
    TABLE_IMPS = [[Counter() for _ in range(4)] for _ in range(4)]
    TABLE_MP = Payoff(("pass1N", "bid3N", "transfer_game", "transfer_invite"), matchpoints)

def accept(deal):
    return is_1nt(deal.north)

def do(deal):
    n = deal.north
    
    # --- Scores for IMPs (Vulnerable) ---
    v = True
    si0 = deal.dd_score("1NN", vul=v)
    si1 = deal.dd_score("3NN", vul=v)
    si4s = deal.dd_score("4SN", vul=v)
    si3s = deal.dd_score("3SN", vul=v)
    si2n = deal.dd_score("2NN", vul=v)
    
    # Strategy 2: Transfer to Game (4S if 3+ spades, else 3NT)
    si_tg = si4s if len(n.spades) >= 3 else si1
    
    # Strategy 3: Transfer Invite (Based on North HCP and Spades)
    if len(n.spades) >= 3:
        si_ti = si4s if n.hcp >= 16 else si3s
    else:
        si_ti = si1 if n.hcp >= 16 else si2n
            
    scores_imps = [si0, si1, si_tg, si_ti]
    for i in range(4):
        for j in range(4):
            TABLE_IMPS[i][j][imps(scores_imps[i], scores_imps[j])] += 1

    # --- Scores for MP (Non-Vulnerable) ---
    v = False
    sm0 = deal.dd_score("1NN", vul=v)
    sm1 = deal.dd_score("3NN", vul=v)
    sm4s = deal.dd_score("4SN", vul=v)
    sm3s = deal.dd_score("3SN", vul=v)
    sm2n = deal.dd_score("2NN", vul=v)
    
    sm_tg = sm4s if len(n.spades) >= 3 else sm1
    
    if len(n.spades) >= 3:
        sm_ti = sm4s if n.hcp >= 16 else sm3s
    else:
        sm_ti = sm1 if n.hcp >= 16 else sm2n
            
    scores_mp = dict(pass1N=sm0, bid3N=sm1, transfer_game=sm_tg, transfer_invite=sm_ti)
    TABLE_MP.add_data(scores_mp)

def final(n_tries):
    print(f"--- TRANSFER STRATEGY COMPARISON ({n_tries} tries) ---")
    print(f"Hand: J9875 K5 Q873 KJ (10 HCP, 5-2-4-2)")
    print(f"Strategies: [0: Pass, 1: 3N, 2: T-Game, 3: T-Invite]")
    
    print("\n1. AVG IMP GAIN (Row over Column):")
    header = "\t" + "\t".join(map(str, range(4)))
    print(header)
    for i, line in enumerate(TABLE_IMPS):
        results = []
        for counter in line:
            total_imps = sum(val * count for val, count in counter.items())
            num_deals = sum(counter.values())
            results.append(f"{total_imps / num_deals:+.2f}")
        print(f"{i}\t" + "\t".join(results))
        
    print("\n2. MATCH POINT (BAM) PAYOFF TABLE:")
    TABLE_MP.report()

if __name__ == "__main__":
    import time
    start = time.time()
    n = 1000
    initial()
    dealer = Deal.prepare(predeal)
    for i in range(n):
        deal = dealer(accept_func=accept)
        do(deal)
    final(n)
    print(f"Simulation took {time.time() - start:.2f}s")

from collections import Counter
from redeal import *

# South hand: 7542 J975 K97 KQ (9 HCP, 4-4-3-2)
predeal = {"S": "7542 J975 K97 KQ"}

def initial():
    global TABLE_IMPS, TABLE_MP
    # Compare 6 strategies:
    # 0: Pass 1NT
    # 1: Bid 3NT
    # 2: Stayman to Game (Always 4M/3NT)
    # 3: Stayman to Invite (Always 2M/2NT)
    # 4: Selective Aggro (4M/3NT if N=16-17, else 3M/2NT)
    # 5: Selective Safe (4M/3NT if N=16-17, else 3M/Pass 2NT)
    
    # For IMPs we use a custom table for better granularity
    TABLE_IMPS = [[Counter() for _ in range(6)] for _ in range(6)]
    # For MP we use the Payoff class
    TABLE_MP = Payoff(("pass1N", "bid3N", "stayman_game", "stayman_invite", "selective_aggro", "selective_safe"), matchpoints)

def accept(deal):
    # North opens 1NT: Using refined is_1nt function
    return is_1nt(deal.north)

def do(deal):
    n = deal.north
    
    # --- Scores for IMPs (Vulnerable) ---
    v = True
    si0 = deal.dd_score("1NN", vul=v)
    si1 = deal.dd_score("3NN", vul=v)
    si4h = deal.dd_score("4HN", vul=v)
    si4s = deal.dd_score("4SN", vul=v)
    si3h = deal.dd_score("3HN", vul=v)
    si3s = deal.dd_score("3SN", vul=v)
    si2h = deal.dd_score("2HN", vul=v)
    si2s = deal.dd_score("2SN", vul=v)
    si2n = deal.dd_score("2NN", vul=v)
    
    # Strategy 2: Stayman to Game (Always 4M/3NT)
    si_sg = si4h if len(n.hearts) >= 4 else (si4s if len(n.spades) >= 4 else si1)
    # Strategy 3: Stayman to Invite (Always 2M/2NT)
    si_si = si2h if len(n.hearts) >= 4 else (si2s if len(n.spades) >= 4 else si2n)
    # Strategy 4/5 logic
    if n.hcp >= 16:
        si_sa = si_ss = si_sg
    else:
        if len(n.hearts) >= 4: si_sa = si_ss = si3h
        elif len(n.spades) >= 4: si_sa = si_ss = si3s
        else:
            si_sa = si2n # Bids 2NT invite
            si_ss = si0  # Passes 1NT (Selective Safe)
            
    scores_imps = [si0, si1, si_sg, si_si, si_sa, si_ss]
    for i in range(6):
        for j in range(6):
            TABLE_IMPS[i][j][imps(scores_imps[i], scores_imps[j])] += 1

    # --- Scores for MP (Non-Vulnerable) ---
    v = False
    sm0 = deal.dd_score("1NN", vul=v)
    sm1 = deal.dd_score("3NN", vul=v)
    sm4h = deal.dd_score("4HN", vul=v)
    sm4s = deal.dd_score("4SN", vul=v)
    sm3h = deal.dd_score("3HN", vul=v)
    sm3s = deal.dd_score("3SN", vul=v)
    sm2h = deal.dd_score("2HN", vul=v)
    sm2s = deal.dd_score("2SN", vul=v)
    sm2n = deal.dd_score("2NN", vul=v)
    
    sm_sg = sm4h if len(n.hearts) >= 4 else (sm4s if len(n.spades) >= 4 else sm1)
    sm_si = sm2h if len(n.hearts) >= 4 else (sm2s if len(n.spades) >= 4 else sm2n)
    if n.hcp >= 16:
        sm_sa = sm_ss = sm_sg
    else:
        if len(n.hearts) >= 4: sm_sa = sm_ss = sm3h
        elif len(n.spades) >= 4: sm_sa = sm_ss = sm3s
        else:
            sm_sa = sm2n
            sm_ss = sm0 # Pass 1NT
            
    scores_mp = dict(pass1N=sm0, bid3N=sm1, stayman_game=sm_sg, stayman_invite=sm_si, selective_aggro=sm_sa, selective_safe=sm_ss)
    TABLE_MP.add_data(scores_mp)

def final(n_tries):
    print(f"--- COMBINED EVALUATION RESULTS ({n_tries} tries) ---")
    print(f"Hand: 7542 J975 K97 KQ (9 HCP, 4-4-3-2)")
    print(f"Against 1NT opener (Refined is_1nt rules)")
    print(f"Strategies: [0: Pass, 1: 3N, 2: S-Game, 3: S-Invite, 4: S-Aggro, 5: S-Safe]")
    
    print("\n1. AVG IMP GAIN (Row over Column):")
    header = "\t" + "\t".join(map(str, range(6)))
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
    # Run the simulation
    # Using Simulation class from redeal
    sim = Simulation()
    sim.initial = initial
    sim.accept = accept
    sim.do = do
    sim.final = final
    
    # We can't easily use redeal.redeal.main because we are a script.
    # We will manually run it.
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

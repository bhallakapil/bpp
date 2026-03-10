from collections import Counter
from redeal import *

# South hand: 7542 J975 K97 KQ
predeal = {"S": "7542 J975 K97 KQ"}

def initial():
    global TABLE
    # Compare 6 strategies for IMPs:
    # 0: Pass 1NT
    # 1: Bid 3NT
    # 2: Stayman to Game (Always 4M/3NT)
    # 3: Stayman to Invite (Always 2M/2NT)
    # 4: Selective Aggro (4M/3NT if N=16-17, else 3M/2NT)
    # 5: Selective Safe (4M/3NT if N=16-17, else 3M/Pass 2NT)
    TABLE = [[Counter() for _ in range(6)] for _ in range(6)]

def accept(deal):
    # North opens 1NT: 15-17 HCP, Balanced
    return 15 <= deal.north.hcp <= 17 and balanced(deal.north)

def do(deal):
    n = deal.north
    # Calculate scores (Vulnerable for IMPs)
    v = True
    score0 = deal.dd_score("1NN", vul=v)
    score1 = deal.dd_score("3NN", vul=v)
    
    # Pre-calculate common scores
    s4h = deal.dd_score("4HN", vul=v)
    s4s = deal.dd_score("4SN", vul=v)
    s3h = deal.dd_score("3HN", vul=v)
    s3s = deal.dd_score("3SN", vul=v)
    s2h = deal.dd_score("2HN", vul=v)
    s2s = deal.dd_score("2SN", vul=v)
    s3n = score1
    s2n = deal.dd_score("2NN", vul=v)
    
    # Strategy 2: Stayman to Game
    if len(n.hearts) >= 4:
        score2 = s4h
    elif len(n.spades) >= 4:
        score2 = s4s
    else:
        score2 = s3n
        
    # Strategy 3: Stayman to Invite (Always 2M/2NT)
    if len(n.hearts) >= 4:
        score3 = s2h
    elif len(n.spades) >= 4:
        score3 = s2s
    else:
        score3 = s2n

    # Strategy 4: Selective Aggro (4M/3NT if N=16-17, else 3M/2NT)
    if n.hcp >= 16:
        score4 = score2
    else:
        if len(n.hearts) >= 4:
            score4 = s3h
        elif len(n.spades) >= 4:
            score4 = s3s
        else:
            score4 = s2n
            
    # Strategy 5: Selective Safe (4M/3NT if N=16-17, else 3M/Pass 2NT)
    if n.hcp >= 16:
        score5 = score2
    else:
        if len(n.hearts) >= 4:
            score5 = s3h
        elif len(n.spades) >= 4:
            score5 = s3s
        else:
            score5 = s2n
            
    scores = [score0, score1, score2, score3, score4, score5]
    
    for i, scorei in enumerate(scores):
        for j, scorej in enumerate(scores):
            TABLE[i][j][imps(scorei, scorej)] += 1

def final(n_tries):
    print(f"--- IMP COMPARISON RESULTS ({n_tries} tries) ---")
    print(f"Hand: 7542 J975 K97 KQ (9 HCP, 4-4-3-2)")
    print(f"Against 1NT opener (15-17 HCP, Balanced)")
    print(f"Strategies: [0: Pass, 1: 3N, 2: S-Game, 3: S-Invite, 4: S-Aggro, 5: S-Safe]")
    print("\nAvg IMPs gain of Row over Column:")
    header = "\t" + "\t".join(map(str, range(6)))
    print(header)
    for i, line in enumerate(TABLE):
        results = []
        for counter in line:
            total_imps = sum(val * count for val, count in counter.items())
            num_deals = sum(counter.values())
            results.append(f"{total_imps / num_deals:.2f}" if num_deals > 0 else "0.00")
        print(f"{i}\t" + "\t".join(results))

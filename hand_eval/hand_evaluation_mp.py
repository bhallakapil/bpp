from redeal import *

# South hand: 7542 J975 K97 KQ
predeal = {"S": "7542 J975 K97 KQ"}

def initial():
    global TABLE
    # Compare 5 strategies:
    # 0: Pass 1NT
    # 1: Bid 3NT
    # 2: Stayman to Game (Always 4M/3NT)
    # 3: Stayman to Invite (Always 2M/2NT)
    # 4: Selective Game (4M/3NT if N=16-17, else 3M/2NT)
    # 5: Selective Game (4M/3NT if N=16-17, else 3M/Pass 2NT)
    TABLE = Payoff(("pass1N", "bid3N", "stayman_game", "stayman_invite", "selective_aggro", "selective_safe"), matchpoints)

def accept(deal):
    # North opens 1NT: 15-17 HCP, Balanced
    return 15 <= deal.north.hcp <= 17 and balanced(deal.north)

def do(deal):
    n = deal.north
    # Calculate scores (Non-vulnerable)
    score_pass1n = deal.dd_score("1NN")
    score_bid3n = deal.dd_score("3NN")
    
    # Pre-calculate common scores
    s4h = deal.dd_score("4HN")
    s4s = deal.dd_score("4SN")
    s3h = deal.dd_score("3HN")
    s3s = deal.dd_score("3SN")
    s2h = deal.dd_score("2HN")
    s2s = deal.dd_score("2SN")
    s3n = score_bid3n
    s2n = deal.dd_score("2NN")
    
    # Strategy 2: Stayman to Game (Always 4M/3NT)
    if len(n.hearts) >= 4:
        score_sg = s4h
    elif len(n.spades) >= 4:
        score_sg = s4s
    else:
        score_sg = s3n
        
    # Strategy 3: Stayman to Invite (Always 2M/2NT)
    if len(n.hearts) >= 4:
        score_si = s2h
    elif len(n.spades) >= 4:
        score_si = s2s
    else:
        score_si = s2n

    # Strategy 4: Selective Aggro (4M/3NT if N=16-17, else 3M/2NT)
    if n.hcp >= 16:
        score_sa = score_sg # Game
    else:
        # Invite to level 3
        if len(n.hearts) >= 4:
            score_sa = s3h
        elif len(n.spades) >= 4:
            score_sa = s3s
        else:
            score_sa = s2n
            
    # Strategy 5: Selective Safe (4M/3NT if N=16-17, else 3M/Pass 2NT)
    if n.hcp >= 16:
        score_ss = score_sg # Game
    else:
        # Pass or invite
        if len(n.hearts) >= 4:
            score_ss = s3h
        elif len(n.spades) >= 4:
            score_ss = s3s
        else:
            score_ss = s2n # "Pass" at 2NT
            
    scores = dict(pass1N=score_pass1n, bid3N=score_bid3n, 
                  stayman_game=score_sg, 
                  stayman_invite=score_si,
                  selective_aggro=score_sa,
                  selective_safe=score_ss)
    TABLE.add_data(scores)

def final(n_tries):
    print(f"--- MATCH POINT (BAM) COMPARISON RESULTS ({n_tries} tries) ---")
    print(f"Hand: 7542 J975 K97 KQ (9 HCP, 4-4-3-2)")
    print(f"Against 1NT opener (15-17 HCP, Balanced)")
    TABLE.report()

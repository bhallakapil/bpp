from redeal import *
from pprint import pprint

# --- Constructed Deal to fit constraints ---
# South (S): 8 HCP (J, J, A, Q present), Shape 4-4-3-2.
# S: S: J987(1), H: J654(1), D: A87(4), C: Q6(2). Total 8 HCP.
s_ranks_dict = {'S': "J987", 'H': "J654", 'D': "A87", 'C': "Q6"}
s_hand = Hand(s_ranks_dict, 8)

# North (N): 16 HCP, balanced (4333 assumed).
# N: S: KQ2T(5), H: AK9(7), D: K54(3), C: J32(1). Total 16 HCP.
n_ranks_dict = {'S': "KQ2T", 'H': "AK9", 'D': "K54", 'C': "J32"}
n_hand = Hand(n_ranks_dict, 16)

# Remaining ranks for E/W (Total 26 cards remaining)
# S (5 left): {A, 6, 5, 4, 3}
# H (6 left): {Q, T, 8, 7, 3, 2}
# D (7 left): {Q, J, T, 9, 6, 3, 2}
# C (8 left): {A, K, T, 9, 8, 7, 5, 4}

# E/W Split (E: 2,3,3,5 | W: 3,3,4,3) - Total 13 cards each
e_s_ranks = "A6"
w_s_ranks = "543"

e_h_ranks = "QT8"
w_h_ranks = "732"

e_d_ranks = "QJT"
w_d_ranks = "9632"

e_c_ranks = "AK987" # E gets 5 C cards: A, K, 9, 8, 7 (4+3+1+1=9 HCP) -> Wait, this is wrong. C: A(4), K(3). Total 7 HCP from C.
# E HCP Check: S:A(4). D:Q(2). C:A(4)+K(3). Total E HCP: 4+2+7 = 13 HCP.
# W HCP must be 16 - 13 = 3 HCP.

e_hand = Hand({'S': e_s_ranks, 'H': e_h_ranks, 'D': e_d_ranks, 'C': e_c_ranks}, 13)

# W HCP: 3.
w_hand = Hand({'S': w_s_ranks, 'H': w_h_ranks, 'D': w_d_ranks, 'C': w_c_ranks}, 3)

# Define the Deal object
deal = Deal(n_hand, e_hand, s_hand, w_hand)

# Contracts to check (assuming they are made)
VULNERABLE = True
scores = {}

# Contract 1: 1NT (North declarer, 9 tricks needed)
score_1nt = deal.dd_score("1NT", vulnerable=VULNERABLE)
scores["1NT (Pass)"] = score_1nt

# Contracts 2-5 (South bidding) - Assume South becomes declarer if they bid.
score_2n = deal.dd_score("2NN", vulnerable=VULNERABLE)
scores["2NT (Bid 2N)"] = score_2n

score_3n = deal.dd_score("3NN", vulnerable=VULNERABLE)
scores["3NT (Bid 3N)"] = score_3n

score_4h = deal.dd_score("4H", vulnerable=VULNERABLE)
scores["4H (Bid 4H)"] = score_4h

score_4s = deal.dd_score("4S", vulnerable=VULNERABLE)
scores["4S (Bid 4S)"] = score_4s

print("--- IMP Vulnerable Scores (Assuming Contract Made) ---")
pprint(scores)

# Check tricks required for the contracts if they were made (for context)
tricks_1nt = deal.dd_tricks("1NT")
tricks_2n = deal.dd_tricks("2NN")
tricks_3n = deal.dd_tricks("3NN")
tricks_4h = deal.dd_tricks("4H")
tricks_4s = deal.dd_tricks("4S")

print("\n--- Double Dummy Tricks for Made Contracts ---")
print(f"1NT Tricks: {tricks_1nt}")
print(f"2NT Tricks: {tricks_2n}")
print(f"3NT Tricks: {tricks_3n}")
print(f"4H Tricks: {tricks_4h}")
print(f"4S Tricks: {tricks_4s}")
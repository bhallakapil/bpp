from redeal import bigdeal, Hand, A, K, Suit
from collections import Counter

def get_normalized_shape(hand):
    return tuple(sorted(hand.shape, reverse=True))

def has_ak_singleton(hand):
    for holding in hand:
        if len(holding) == 1:
            if A in holding or K in holding:
                return True
    return False

def is_54_majors(hand):
    s = len(hand.spades)
    h = len(hand.hearts)
    return (s == 5 and h == 4) or (s == 4 and h == 5)

def has_6_card_major(hand):
    return len(hand.spades) >= 6 or len(hand.hearts) >= 6

def opens_1nt_new_rules(hand):
    shape = get_normalized_shape(hand)
    balanced = {(4, 4, 3, 2), (5, 3, 3, 2), (4, 3, 3, 3)}
    
    if shape in balanced:
        return True
    
    if shape == (5, 4, 2, 2):
        if is_54_majors(hand): return False
        return True
        
    if shape == (6, 3, 2, 2):
        return False
        
    if shape == (5, 4, 3, 1):
        if is_54_majors(hand): return False
        return has_ak_singleton(hand)
        
    if shape == (4, 4, 4, 1):
        return has_ak_singleton(hand)
        
    return False

def run_simulation(n=5000000):
    counts_15_17 = Counter()
    opens_15_17 = Counter()
    counts_20_21 = Counter()
    opens_20_21 = Counter()
    
    total_15_17 = 0
    total_20_21 = 0
    
    for i in range(n // 4):
        deal = bigdeal.get_deal(boardno=i)
        for card_list in deal:
            hand = Hand(card_list)
            hcp = hand.hcp
            shape = get_normalized_shape(hand)
            
            if 15 <= hcp <= 17:
                total_15_17 += 1
                counts_15_17[shape] += 1
                if opens_1nt_new_rules(hand):
                    opens_15_17[shape] += 1
            elif 20 <= hcp <= 21:
                total_20_21 += 1
                counts_20_21[shape] += 1
                if opens_1nt_new_rules(hand):
                    opens_20_21[shape] += 1
                            
    print(f"Total 15-17 HCP: {total_15_17}")
    print(f"Total 20-21 HCP: {total_20_21}")
    
    order = [(4, 4, 3, 2), (5, 3, 3, 2), (5, 4, 3, 1), (5, 4, 2, 2), (4, 3, 3, 3), (4, 4, 4, 1)]
    
    print("\nTable for 15-17 (1NT) vs 20-21 (2NT)")
    print(f"{'Shape':<10} | {'1NT Open %':<12} | {'2NT Open %':<12}")
    print("-" * 40)
    
    total_1nt = 0
    total_2nt = 0
    for shape in order:
        p1 = (opens_15_17[shape] / total_15_17) * 100
        p2 = (opens_20_21[shape] / total_20_21) * 100
        total_1nt += opens_15_17[shape]
        total_2nt += opens_20_21[shape]
        shape_str = "-".join(map(str, shape))
        print(f"{shape_str:<10} | {p1:>10.2f}% | {p2:>10.2f}%")
        
    print("-" * 40)
    print(f"{'TOTAL':<10} | {(total_1nt/total_15_17)*100:>10.2f}% | {(total_2nt/total_20_21)*100:>10.2f}%")

if __name__ == "__main__":
    run_simulation(5000000)

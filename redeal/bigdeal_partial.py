import math
import random
import hashlib
import os

def comb(n, k):
    return math.comb(n, k)

def map_number_to_hand(number, cards, k):
    """
    Maps a number to a selection of k cards from a list of n cards.
    This is the standard algorithm used by bigdeal.
    """
    n = len(cards)
    hand = []
    remaining_cards = []
    
    for card in cards:
        if k > 0 and n > k:
            c = comb(n - 1, k)
            if number < c:
                # Card does NOT go into hand
                remaining_cards.append(card)
            else:
                # Card DOES go into hand
                hand.append(card)
                number -= c
                k -= 1
        elif k > 0:
            # Must take the rest of the cards
            hand.append(card)
            k -= 1
        else:
            # Hand is full
            remaining_cards.append(card)
        n -= 1
        
    return hand, remaining_cards

def generate_partial_deal(cards, needs, seed_bits=None):
    """
    Generates a partial deal for 4 hands given:
    - cards: list of available cards
    - needs: list of number of cards needed for each seat (N, E, S, W)
    - seed_bits: Optional random number bits for the deal
    
    Returns a list of 4 card lists.
    """
    # Calculate total capacity
    R = len(cards)
    capacity = 1
    temp_R = R
    for k in needs[:3]: # Only need first 3 hands, 4th is remainder
        capacity *= comb(temp_R, k)
        temp_R -= k
        
    if seed_bits is None:
        # Use RMD160-based RNG for bridge standard randomness
        # We use os.urandom as entropy source for the RMD160 hash
        seed = os.urandom(64)
        h = hashlib.new('ripemd160', seed).digest()
        # Big deal uses 96 bits, but we can use all 160 bits for better distribution
        number = int.from_bytes(h, 'big') % capacity
    else:
        number = seed_bits % capacity
        
    hands = [[] for _ in range(4)]
    current_cards = sorted(cards) # Ensure deterministic mapping
    
    for i in range(3):
        k = needs[i]
        if k > 0:
            # We need to split the current number G' into (G_i, G_rest)
            # G' = G_i * (capacity of rest) + G_rest
            # This is not exactly how bigdeal does it (it uses one large number).
            # bigdeal approach:
            # G = Goedel number
            # For each hand i:
            #   C_i = capacity of hand i given remaining cards
            #   Hand i selection is based on G % C_i
            #   G = G // C_i
            
            # Re-implementing bigdeal-style mapping:
            c_i = comb(len(current_cards), k)
            current_number = number % c_i
            number //= c_i
            
            hand_cards, current_cards = map_number_to_hand(current_number, current_cards, k)
            hands[i] = hand_cards
        else:
            hands[i] = []
            
    hands[3] = current_cards # Remainder goes to West
    return hands

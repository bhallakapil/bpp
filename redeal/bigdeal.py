import hashlib
import os
import math
import random
from .global_defs import Card, Rank, Suit

# Cache for entropy, similar to how bigdeal collects it once
_entropy = None

def _get_entropy():
    global _entropy
    if _entropy is None:
        _entropy = os.urandom(20)
    return _entropy

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
            c = math.comb(n - 1, k)
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
        capacity *= math.comb(temp_R, k)
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
            # Re-implementing bigdeal-style mapping:
            c_i = math.comb(len(current_cards), k)
            current_number = number % c_i
            number //= c_i
            
            hand_cards, current_cards = map_number_to_hand(current_number, current_cards, k)
            hands[i] = hand_cards
        else:
            hands[i] = []
            
    hands[3] = current_cards # Remainder goes to West
    return hands

def get_deal(boardno=0, owner=b"redeal"):
    """
    Pure Python implementation of the bigdeal algorithm.
    Generates a full deal for a given board number and owner.
    """
    entropy = _get_entropy()
    owner_hash = hashlib.new('ripemd160', owner).digest()
    
    # Total number of possible bridge deals
    capacity = (math.comb(52, 13) * 
                math.comb(39, 13) * 
                math.comb(26, 13))
    
    seqno = boardno
    while True:
        seqno += 1
        # Replicate bigdeal's seed structure:
        # 4 bytes seqno (LE) + 20 bytes entropy + 20 bytes owner hash
        seed = (seqno.to_bytes(4, 'little') + 
                entropy + 
                owner_hash)
        
        h = hashlib.new('ripemd160', seed).digest()
        # Bigdeal uses the first 12 bytes (96 bits) of the hash as the Goedel number
        number = int.from_bytes(h[:12], 'big')
        
        if number < capacity:
            break
            
    # Standard bigdeal card order: Spades A-2, Hearts A-2, Diamonds A-2, Clubs A-2
    cards = []
    for suit in Suit:
        for rank in sorted(list(Rank), reverse=True):
            cards.append(Card(suit, rank))
            
    # Use the mapping logic
    hands = generate_partial_deal(cards, [13, 13, 13, 13], seed_bits=number)
    return hands

import hashlib
import os
import math
from .global_defs import Card, Rank, Suit
from . import bigdeal_partial

# Cache for entropy, similar to how bigdeal collects it once
_entropy = None

def _get_entropy():
    global _entropy
    if _entropy is None:
        _entropy = os.urandom(20)
    return _entropy

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
            
    # Use the mapping logic from bigdeal_partial
    hands = bigdeal_partial.generate_partial_deal(cards, [13, 13, 13, 13], seed_bits=number)
    return hands

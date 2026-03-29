from redeal import *
import sys

# North's hand: S 6 H JT632 D 72 C QJ987
predeal = {"N": "6 JT632 72 QJ987"}

def accept(deal):
    west = deal.west
    east = deal.east
    
    # West: 1NT opener (15-17), no 5-card major, no 4-card spade suit
    if not is_1nt(west): return False
    if len(west.spades) >= 4: return False
    if len(west.hearts) > 4: return False # At most 4 hearts
    
    # East: 9-15 HCP, 4 spades, at most 3 hearts
    if not (9 <= east.hcp <= 15): return False
    if len(east.spades) != 4: return False
    if len(east.hearts) > 3: return False
    
    return True

# Simulation for 3NT by West (3NW)
# Only evaluating CQ and HJ
class TwoLeadSim(OpeningLeadSim):
    def initial(self, dealer):
        self.payoff = Payoff(
            [Card(Suit.C, Q), Card(Suit.H, J), Card(Suit.H, Rank['3'])],
            self.scoring)

sim = TwoLeadSim(accept, "3NW", matchpoints)

if __name__ == "__main__":
    dealer = Deal.prepare(predeal)
    sim.initial(dealer)
    
    count = 0
    target = 2000 # More samples for a more precise comparison
    while count < target:
        try:
            deal = dealer(accept_func=accept, tries=10000)
            sim.do(deal)
            count += 1
            if count % 200 == 0:
                print(f"Progress: {count}/{target}", file=sys.stderr)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            break
            
    sim.final(count)

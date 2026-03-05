from redeal import *
from redeal import global_defs

# S: AQ3 H KJT83 D T6 C AQ2
predeal = {"S": "AQ3 KJT83 T6 AQ2"}

def accept(deal):
    # We fix the hand, so we accept all deals generated.
    return True 

class EvaluateSHand(Simulation):
    def __init__(self):
        pass

    def initial(self, dealer):
        # Force generation of the specific deal with predealt South hand
        dealer_override = Deal.prepare(predeal)
        self.deal = next(iter(dealer_override, None))
        
    def do(self, deal):
        # We only process the one deal generated in initial
        pass

    def final(self, n_tries):
        s_hand = self.deal.south
        s_hcp = s_hand.hcp
        s_shape = s_hand.shape # (3, 5, 2, 3) based on S,H,D,C order
        
        print(f"South Hand: {s_hand}")
        print(f"HCP: {s_hcp}, Shape (S,H,D,C): {s_shape}")
        print("-" * 30)
        
        # 1. Evaluate 1H contract (South declares)
        tricks_1h = self.deal.dd_tricks("1HS")
        # Contract is available from 'from redeal import *'
        score_1h = Contract(1, "H", 0, False).score(tricks_1h)
        
        # 2. Evaluate 1NT contract (South declares)
        tricks_1nt = self.deal.dd_tricks("1NNS")
        score_1nt = Contract(1, "N", 0, False).score(tricks_1nt)
        
        print(f"Double Dummy Evaluation (South Declares):")
        print(f"1H makes {tricks_1h} tricks, Score: {score_1h}")
        print(f"1NT makes {tricks_1nt} tricks, Score: {score_1nt}")
        print("-" * 30)
        
        if score_1h > score_1nt:
            print("Conclusion: Opening 1H is likely more beneficial than 1NT.")
        elif score_1nt > score_1h:
            print("Conclusion: Opening 1NT is likely more beneficial than 1H.")
        else:
            print("Conclusion: Both contracts result in the same DD score.")

if __name__ == "__main__":
    # Set style to long for good hand printing
    Deal.set_str_style("long")
    Hand.set_str_style("long")
    
    sim = EvaluateSHand()
    dealer = Deal.prepare(predeal)
    
    # Manually execute initial setup (which forces the deal)
    sim.initial(dealer)
    
    # Manually execute final report
    sim.final(1)

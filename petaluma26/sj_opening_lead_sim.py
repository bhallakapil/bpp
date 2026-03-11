from redeal import *
import sys

# South's hand: S AJ10953 H J1073 D 103 C 4
predeal = {"S": "AJT953 JT73 T3 4"}

def accept(deal):
    east = deal.east
    west = deal.west
    
    # East: 20-21 HCP, balanced or semi-balanced
    if not is_2nt(east):
        return False
        
    # West: 3-12 HCP
    if not (3 <= west.hcp <= 12):
        return False
        
    # West: can have 4333 or 3433 hand, or <=3 in majors
    sw, hw, dw, cw = west.shape
    if (sw > 3 or hw > 3) and not (west.shape == (4,3,3,3) or west.shape == (3,4,3,3)):
        return False

    # West: no voids, no suit > 6, two longest suits <= 9
    if 0 in west.shape or max(west.shape) > 6 or sum(sorted(west.shape)[2:]) > 9:
        return False
        
    return True

class DualOpeningLeadSim(Simulation):
    def __init__(self, accept, contract_declarer):
        self.accept = accept
        self.leader = (Seat[contract_declarer[-1]] + 1).name
        contract = Contract.from_str(contract_declarer[:-1])
        self.strain = contract.strain
        
        # Define scoring functions
        # Note: ti and tj are defense tricks (returned by dds.solve_all),
        # so 13-ti is declarer tricks.
        self.imps_scoring = lambda ti, tj: -imps(contract.score(13-ti), contract.score(13-tj))
        self.mps_scoring = lambda ti, tj: -matchpoints(contract.score(13-ti), contract.score(13-tj))
        
    def initial(self, dealer):
        # Pick the first accepted deal to find the available leads
        deal = next(filter(self.accept, iter(dealer, None)))
        leads = sorted(dds.valid_cards(deal, self.strain, self.leader), reverse=True)
        self.payoff_imps = Payoff(leads, self.imps_scoring)
        self.payoff_mps = Payoff(leads, self.mps_scoring)

    def do(self, deal):
        # Get defense tricks for all leads
        tricks = deal.dd_all_tricks(self.strain, self.leader)
        self.payoff_imps.add_data(tricks)
        self.payoff_mps.add_data(tricks)

    def final(self, n_tries):
        print("\n### Simulation Results (IMPs):")
        self.payoff_imps.report()
        print("\n### Simulation Results (Matchpoints):")
        self.payoff_mps.report()

if __name__ == "__main__":
    dealer = Deal.prepare(predeal)
    sim = DualOpeningLeadSim(accept, "3NE")
    sim.initial(dealer)
    
    n_samples = 10000
    count = 0
    print(f"Starting dual simulation for {n_samples} samples...", file=sys.stderr)
    
    for i in range(1, 1000000):
        if count >= n_samples:
            break
        try:
            deal = dealer()
            if accept(deal):
                sim.do(deal)
                count += 1
                if count % 200 == 0:
                    print(f"Progress: {count}/{n_samples}", file=sys.stderr)
        except Exception:
            continue
            
    sim.final(count)

from redeal import *
import sys
from collections import Counter

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
    def __init__(self, accept, contract_declarer, save_hands_path=None):
        self.accept = accept
        self.leader = (Seat[contract_declarer[-1]] + 1).name
        self.contract = Contract.from_str(contract_declarer[:-1])
        self.strain = self.contract.strain
        self.save_hands_path = save_hands_path
        self.saved_hands_count = 0
        self.spade_breaks = Counter()
        
        # Define scoring functions
        self.imps_scoring = lambda ti, tj: -imps(self.contract.score(13-ti), self.contract.score(13-tj))
        self.mps_scoring = lambda ti, tj: -matchpoints(self.contract.score(13-ti), self.contract.score(13-tj))
        
    def initial(self, dealer):
        # Pick the first accepted deal
        deal = next(filter(self.accept, iter(dealer, None)))
        
        # User requested specific leads to compare against SJ
        target_leads_strs = ["SJ", "HJ", "H3", "DT", "C4"] 
        target_leads = [Card.from_str(s) for s in target_leads_strs]
        
        # Verify they are in the hand
        south_hand = deal[Seat[self.leader]]
        leads = [c for c in target_leads if c in south_hand]
        
        if not leads:
            leads = sorted(dds.valid_cards(deal, self.strain, self.leader), reverse=True)
        
        self.payoff_imps = Payoff(leads, self.imps_scoring)
        self.payoff_mps = Payoff(leads, self.mps_scoring)
        
        if self.save_hands_path:
            with open(self.save_hands_path, 'w') as f:
                f.write(f"Simulation hands for {self.strain} lead by {self.leader}\n")
                f.write(f"Comparing: {', '.join(map(str, leads))} against {leads[0]}\n")
                f.write("="*40 + "\n")

    def do(self, deal):
        # Get defense tricks for all leads
        tricks = deal.dd_all_tricks(self.strain, self.leader)
        
        all_tricks = {}
        for suit in Suit:
            holding = deal[Seat[self.leader]][suit]
            ranks = sorted(holding, reverse=True)
            last_tricks = None
            for rank in ranks:
                card = Card(suit, rank)
                if card in tricks:
                    last_tricks = tricks[card]
                all_tricks[card] = last_tricks
        
        self.payoff_imps.add_data(all_tricks)
        self.payoff_mps.add_data(all_tricks)
        
        # Track spade breaks
        nw_spades = len(deal.north.spades)
        ew_spades = len(deal.east.spades)
        ww_spades = len(deal.west.spades)
        spade_break = tuple(sorted((nw_spades, ew_spades, ww_spades), reverse=True))
        self.spade_breaks[spade_break] += 1
        
        if self.save_hands_path and self.saved_hands_count < 100:
            with open(self.save_hands_path, 'a') as f:
                f.write(f"Hand {self.saved_hands_count + 1}:\n")
                f.write(f"Spade Break: {nw_spades}-{ew_spades}-{ww_spades} (N-E-W)\n")
                
                # HCP and Shape for all hands
                for seat in Seat:
                    hand = deal[seat]
                    shape_str = "-".join(map(str, hand.shape))
                    f.write(f"{seat.name}: HCP {hand.hcp}, Shape {shape_str}\n")
                
                Deal.set_str_style("long")
                f.write(str(deal))
                f.write("\n\nLeads Analysis (vs SJ):\n")
                f.write("Lead\tTricks\tScore\tIMP (vs SJ)\tMP (vs SJ)\n")
                
                leads = self.payoff_imps.entries
                ref_tricks = all_tricks[leads[0]]
                
                for lead in leads:
                    t = all_tricks[lead]
                    score = self.contract.score(13 - t)
                    imp_diff = self.imps_scoring(t, ref_tricks)
                    mp_diff = self.mps_scoring(t, ref_tricks)
                    f.write(f"{lead}\t{t}\t{score}\t{imp_diff:+.1f}\t{mp_diff:+.1f}\n")
                    
                f.write("\n" + "-"*40 + "\n")
            self.saved_hands_count += 1

    def final(self, n_tries):
        print("\n### Simulation Results (IMPs):")
        self.payoff_imps.report()
        print("\n### Simulation Results (Matchpoints):")
        self.payoff_mps.report()
        
        break_summary = "\n### Spade Suit Breaks (North-East-West):\n"
        total = sum(self.spade_breaks.values())
        for break_type, count in self.spade_breaks.most_common():
            percentage = (count / total) * 100
            break_summary += f"{'-'.join(map(str, break_type))}: {count} ({percentage:.1f}%)\n"
        
        print(break_summary)
        
        if self.save_hands_path:
            with open(self.save_hands_path, 'a') as f:
                f.write("\n" + "="*40 + "\n")
                f.write(break_summary)

if __name__ == "__main__":
    dealer = Deal.prepare(predeal)
    sim = DualOpeningLeadSim(accept, "3NE", save_hands_path="petaluma26/analysis/sj_opening_lead_hands.txt")
    sim.initial(dealer)
    
    n_samples = 100
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

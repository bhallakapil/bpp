import sys
import os
import re

# Add current directory to sys.path to allow importing redeal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from redeal import Hand, Rank, Suit, Card, Seat
from redeal.dds import solve_all

def get_suit_tokens(line):
    line = line.replace("—", "-").replace("10", "T")
    parts = re.split(r"\s{2,}", line.strip())
    tokens = []
    for p in parts:
        if not p: continue
        if "-" in p and len(p.replace(" ","")) > 0 and set(p.replace(" ","")) == {"-"}:
            tokens.extend(["-" for _ in range(p.count("-"))])
        else:
            tokens.append(p.strip())
    return tokens

def get_winner(trick_cards, trump):
    lead_card, lead_seat = trick_cards[0]
    best_card, winner_seat = lead_card, lead_seat
    trump_suit = Suit.S if trump == "S" else None
    for c, s in trick_cards[1:]:
        is_new_best = False
        if trump_suit and c.suit == trump_suit:
            if best_card.suit != trump_suit or c.rank > best_card.rank: is_new_best = True
        elif c.suit == lead_card.suit:
            if best_card.suit != trump_suit and c.rank > best_card.rank: is_new_best = True
        if is_new_best: best_card, winner_seat = c, s
    return winner_seat

def simulate_winning_line_ordered(deal, trump, leader_name, first_lead):
    current_deal = list(deal)
    current_leader = Seat[leader_name]
    declarer_seats = {current_leader, current_leader + 2}
    history = []
    lead_card = first_lead
    
    for trick_num in range(1, 6):
        trick_data = {}
        trick_play_order = []
        original_leader = current_leader
        trick_branches = []
        
        # 1. Lead
        trick_data[current_leader] = lead_card
        trick_play_order.append((lead_card, current_leader))
        current_deal[current_leader.value] = Hand([c for c in current_deal[current_leader.value].cards() if c != lead_card])
        
        # 2. Others
        curr_objs = [lead_card]
        for i in range(1, 4):
            player = current_leader + i
            valid = [c for c in current_deal[player.value].cards() if c.suit == curr_objs[0].suit]
            if not valid: valid = current_deal[player.value].cards()
            if not valid: break
            
            # Check branching for defenders
            if player not in declarer_seats and len(valid) > 1:
                outs = {}
                for vc in valid:
                    try:
                        res = solve_all(tuple(current_deal), trump, current_leader.name, current_trick=curr_objs + [vc])
                        outs[vc] = max(res.values()) if res else 0
                    except: pass
                if len(set(outs.values())) > 1:
                    v_sorted = sorted(outs.keys(), key=lambda c: outs[c])
                    branch = f"(If {player} plays {v_sorted[0]}, side wins {outs[v_sorted[0]]} more. Else if {v_sorted[-1]}, side wins {outs[v_sorted[-1]]} more)"
                    trick_branches.append(branch)

            best_c = None
            if player in declarer_seats:
                best_t = -1
                for vc in valid:
                    try:
                        res = solve_all(tuple(current_deal), trump, current_leader.name, current_trick=curr_objs + [vc])
                        t = max(res.values()) if res else 0
                        if t > best_t: best_t = t; best_c = vc
                    except: pass
            else:
                best_t = 99
                for vc in valid:
                    try:
                        res = solve_all(tuple(current_deal), trump, current_leader.name, current_trick=curr_objs + [vc])
                        t = max(res.values()) if res else 0
                        if t < best_t: best_t = t; best_c = vc
                    except: pass
            if best_c is None: best_c = valid[0]
            trick_data[player] = best_c
            trick_play_order.append((best_c, player))
            curr_objs.append(best_c)
            current_deal[player.value] = Hand([c for c in current_deal[player.value].cards() if c != best_c])

        winner = get_winner(trick_play_order, trump)
        parts = []
        for s in [Seat.S, Seat.W, Seat.N, Seat.E]:
            c = trick_data.get(s)
            c_str = str(c) if c else "-"
            if s == original_leader: c_str = f"<u>{c_str}</u>"
            if s == winner: c_str = f"({c_str})"
            parts.append(c_str)
            
        line_out = f"Trick {trick_num}: {', '.join(parts)}."
        if trick_branches: line_out += " " + " ".join(trick_branches)
        history.append(line_out)
        
        current_leader = winner
        if trick_num < 5:
            try:
                leads = solve_all(tuple(current_deal), trump, current_leader.name)
                if not leads: break
                if current_leader in declarer_seats: lead_card = max(leads.items(), key=lambda x: x[1])[0]
                else: lead_card = min(leads.items(), key=lambda x: x[1])[0]
            except: break
    return history

def parse_and_analyze():
    with open("pdf_text.txt", "r") as f:
        content = f.read()
    raw_problems = re.split(r"\n(?=\d{1,2}\.\s*)", content)
    problems = []
    for rp in raw_problems:
        lines = [l.strip() for l in rp.strip().split("\n") if l.strip()]
        if not lines: continue
        match = re.match(r"^(\d+)\.\s*(.*)$", lines[0])
        if not match: continue
        num = int(match.group(1)); title = match.group(2).strip()
        has_win = False; win_idx = -1
        for i in range(1, min(6, len(lines))):
            if "win" in lines[i]: has_win = True; win_idx = i; break
        if not has_win: continue
        all_tokens = []
        trump = "S"; goal = 0; leader = "S"
        for i in range(win_idx, len(lines)):
            l = lines[i]
            if "win" in l:
                if "NT" in l: trump = "N"
                goal_match = re.search(r"win\s+(\d+)", l); 
                if goal_match: goal = int(goal_match.group(1))
                parts = re.split(r"win\s+\d+", l)
                if len(parts) > 1 and parts[1].strip(): all_tokens.extend(get_suit_tokens(parts[1].strip()))
            elif "leads" in l:
                if "South" in l: leader = "S"
                elif "West" in l: leader = "W"
                elif "North" in l: leader = "N"
                elif "East" in l: leader = "E"
                parts = l.split("leads")
                if len(parts) > 1 and parts[1].strip(): all_tokens.extend(get_suit_tokens(parts[1].strip()))
            else: all_tokens.extend(get_suit_tokens(l))
        if len(all_tokens) >= 16:
            problems.append({"num": num, "title": title if title else "Untitled", "trump": trump, "goal": goal, "leader": leader, "holdings": all_tokens[:16]})
    problems.sort(key=lambda x: x["num"])
    
    with open("results.md", "w") as out:
        for p in problems:
            try:
                h = []
                for x in p["holdings"]:
                    xt = x.replace("-", "").replace("10", "T").replace(" ", "")
                    h.append(xt if xt else "-")
                trump_full = "NT" if p["trump"] == "N" else "Spades"
                out.write(f"## {p['num']}. {p['title']}\n- **Goal**: {trump_full} win {p['goal']}\n- **Leader**: {p['leader']}\n\n")
                out.write("```\n" + f"{' ' * 20}North\n" + f"{' ' * 20}S: {h[0]}\n{' ' * 20}H: {h[1]}\n{' ' * 20}D: {h[2]}\n{' ' * 20}C: {h[3]}\n\n")
                out.write(f"West{' ' * 31}East\n")
                labels = ["S:", "H:", "D:", "C:"]
                for i in range(4): out.write(f"{labels[i]} {h[4+i]}".ljust(35) + f"{labels[i]} {h[8+i]}\n")
                out.write(f"\n{' ' * 20}South\n" + f"{' ' * 20}S: {h[12]}\n{' ' * 20}H: {h[13]}\n{' ' * 20}D: {h[14]}\n{' ' * 20}C: {h[15]}\n" + "```\n\n")
                def cr(s): return s.replace("-","").replace("10","T") if s!="-" else "-"
                n_h = Hand.from_str(" ".join(cr(h[i]) for i in range(0,4)))
                w_h = Hand.from_str(" ".join(cr(h[i]) for i in range(4,8)))
                e_h = Hand.from_str(" ".join(cr(h[i]) for i in range(8,12)))
                s_h = Hand.from_str(" ".join(cr(h[i]) for i in range(12,16)))
                deal = (n_h, e_h, s_h, w_h)
                leads = solve_all(deal, p["trump"], p["leader"])
                groups = {}
                for c, t in leads.items(): groups.setdefault(t, []).append(c)
                winning_counts = sorted([t for t in groups.keys() if t >= p["goal"]], reverse=True)
                if winning_counts:
                    out.write("**Winning Lines (S, W, N, E):**\n")
                    for t in winning_counts:
                        cards_str = ", ".join(str(c) for c in groups[t])
                        out.write(f"### Leads: {cards_str} ({t} tricks)\n")
                        history = simulate_winning_line_ordered(deal, p["trump"], p["leader"], groups[t][0])
                        for step in history: out.write(f"- {step}\n")
                        out.write("\n")
                else: out.write("**Result:** No winning line found.\n")
                out.write("\n---\n\n")
            except Exception as ex: out.write(f"## {p['num']}. {p['title']}\nError: {ex}\n\n---\n\n")

if __name__ == "__main__":
    parse_and_analyze()

import sys
import os
import re
import json

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

def simulate_full_play(deal, trump, leader_name, first_lead):
    current_deal = list(deal)
    current_leader = Seat[leader_name]
    declarer_seats = {current_leader, current_leader + 2}
    history = []
    lead_card = first_lead
    
    for trick_num in range(1, 6):
        trick_cards = []
        curr_objs = [lead_card]
        trick_cards.append((lead_card, current_leader))
        current_deal[current_leader.value] = Hand([c for c in current_deal[current_leader.value].cards() if c != lead_card])
        
        for i in range(1, 4):
            player = current_leader + i
            valid = [c for c in current_deal[player.value].cards() if c.suit == curr_objs[0].suit]
            if not valid: valid = current_deal[player.value].cards()
            if not valid: break
            
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
            trick_cards.append((best_c, player))
            curr_objs.append(best_c)
            current_deal[player.value] = Hand([c for c in current_deal[player.value].cards() if c != best_c])
            
        winner = get_winner(trick_cards, trump)
        history.append({"trick": trick_num, "cards": [str(c) for c, s in trick_cards], "winner": str(winner)})
        current_leader = winner
        if trick_num < 5:
            try:
                leads = solve_all(tuple(current_deal), trump, current_leader.name)
                if not leads: break
                if current_leader in declarer_seats: lead_card = max(leads.items(), key=lambda x: x[1])[0]
                else: lead_card = min(leads.items(), key=lambda x: x[1])[0]
            except: break
    return history

def analyze_all_to_json():
    with open("pdf_text.txt", "r") as f:
        content = f.read()
    raw_problems = re.split(r"\n(?=\d{1,2}\.\s*)", content)
    problems_data = []
    for rp in raw_problems:
        lines = [l.strip() for l in rp.strip().split("\n") if l.strip()]
        if not lines: continue
        match = re.match(r"^(\d+)\.\s+(.*)$", lines[0])
        if not match: continue
        num = int(match.group(1)); title = match.group(2).strip()
        if num < 1 or num > 88: continue
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
            problems_data.append({"num": num, "title": title, "trump": trump, "goal": goal, "leader": leader, "holdings": all_tokens[:16]})

    results = []
    for p in sorted(problems_data, key=lambda x: x["num"]):
        print(f"Analyzing Board {p['num']}...")
        board_res = {"num": p["num"], "title": p["title"], "leads": []}
        try:
            h = [x.replace("-","").replace("10","T").replace(" ","") if x!="-" else "-" for x in p["holdings"]]
            n_h = Hand.from_str(" ".join(h[i] if h[i]!="-" else "-" for i in range(0,4)))
            w_h = Hand.from_str(" ".join(h[i] if h[i]!="-" else "-" for i in range(4,8)))
            e_h = Hand.from_str(" ".join(h[i] if h[i]!="-" else "-" for i in range(8,12)))
            s_h = Hand.from_str(" ".join(h[i] if h[i]!="-" else "-" for i in range(12,16)))
            deal = (n_h, e_h, s_h, w_h)
            
            leads_eval = solve_all(deal, p["trump"], p["leader"])
            for l_card, tricks in leads_eval.items():
                play_history = simulate_full_play(deal, p["trump"], p["leader"], l_card)
                board_res["leads"].append({
                    "lead": str(l_card),
                    "tricks": tricks,
                    "play": play_history
                })
        except Exception as e:
            board_res["error"] = str(e)
        results.append(board_res)

    with open("analysis_data.json", "w") as out:
        json.dump(results, out, indent=2)

if __name__ == "__main__":
    analyze_all_to_json()

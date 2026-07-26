# Rule of 8 Simulation Analysis, LTC & Statistics

This document provides a comprehensive statistical, Loser Trick Count (LTC), and strategic analysis of the **Rule of 8** bridge simulation model implemented in [`analysis/mels_rules/ruleof8_simulation.py`](analysis/mels_rules/ruleof8_simulation.py).

## Simulation Architecture & Parameters
1. **South Open 1NT**: South opens 1NT (15–17 HCP, balanced/semi-balanced shapes as defined by [`is_1nt()`](redeal/redeal.py:560)).
2. **North Pass**: North has any hand (no constraints) and passes over 1NT.
3. **West Overcall 2H / 2S**: West holds either a 5-3-3-2 shape (with a 5-card major) or a single-suited shape from [`analysis/cumulative_shape_probabilities.md`](analysis/cumulative_shape_probabilities.md), where the longest suit is Spades or Hearts.
4. **Minimum HCP & LTC Threshold**: West holds at least 6 HCP and satisfies the Rule of 8 / length & loser condition: `(l1 + l2 - losers) >= 2`.
5. **East Pass**: East passes unconditionally.
6. **Double Dummy & Par Comparison**: Each deal is evaluated using Double Dummy Solver (DDS) tricks to calculate West's actual contract score in 2H or 2S versus the optimal board par score (`deal.par()`).

---

## Detailed Statistical & LTC Analysis

### 1. Overall Performance & Success Rate
- **Par or Better Rate**: **63.69%** (across large-scale simulation of 7,260 accepted deals out of 10M iterations) of simulated deals achieve the optimal par score or better for East-West when West overcalls under Rule of 8.
- **Suit Breakdown**: West overcalls Spades (49.75%) and Hearts (50.25%) almost equally.

### 2. West Hand Characteristics & LTC
- **Average Loser Trick Count (LTC)**: **~6.58** losers, demonstrating that West overcalls under this rule are tightly controlled around constructive 6-7 loser hands.
- **Average Longest Suit Length ($l_1$)**: **~6.30** cards.
- **Average Controls** ($A=2, K=1$): **~2.95** controls per overcall.

### 3. High Card Point (HCP) Distribution Across Seats
- **South (1NT Opener)**: ~15.65 HCP
- **West (Overcaller)**: ~10.20 HCP average (concentrated between 7 and 12 HCP)
- **East (Partner)**: ~7.10 HCP
- **North (Opener's Partner)**: ~7.05 HCP

---

## Hand Examples: Better or Equal to Par (3 Examples)

1. **West 2S Score: +110, EW Par: -460** (Par Contract: 4NS+1)
   - *Analysis*: West's 2S overcall disrupts NS game bidding, resulting in a positive score (+110) while preventing opponents from collecting their optimal game par.
   - *Hands*:
     - North: `S:                 H: AQJ432          D: A98             C: J842`
     - West:  `S: KQ98753         H: 76              D: 32              C: K3`
     - East:  `S: J62             H: T985            D: 765             C: A96`
     - South: `S: AT4             H: K               D: KQJT4           C: QT75`

2. **West 2S Score: -50, EW Par: -450** (Par Contract: 4HS+1)
   - *Analysis*: West enters at 2S and takes a minimal penalty (-50) compared to the opponents' making game par (-450).
   - *Hands*:
     - North: `S: A85             H: J7643           D: 983             C: K7`
     - West:  `S: K97432          H: 9               D: J4              C: A432`
     - East:  `S: T6              H: T85             D: AT765           C: QJ9`
     - South: `S: QJ              H: AKQ2            D: KQ2             C: T865`

3. **West 2H Score: +140, EW Par: -300** (Par Contract: 5HXW-2)
   - *Analysis*: West makes 2H with overtricks (+140) outperforming the defensive par expectation.
   - *Hands*:
     - North: `S: 72              H: 8               D: AJ87542         C: Q96`
     - West:  `S: QJT4            H: QT6432          D: Q               C: T4`
     - East:  `S: K9863           H: KJ75            D: 9               C: A82`
     - South: `S: A5              H: A9              D: KT63            C: KJ753`

---

## Hand Examples: Worse than Par (3 Examples)

1. **West 2H Score: +110, EW Par: +300** (Par Contract: 4DXS-2)
   - *Analysis*: West makes 2H (+110), but defense against opponents' minor suit contract would have yielded a larger plus score (+300).
   - *Hands*:
     - North: `S: J974            H:                 D: QT7652          C: 873`
     - West:  `S: KT6             H: AQJ932          D: J4              C: 94`
     - East:  `S: Q8              H: 85              D: 983             C: AKJ52`
     - South: `S: A32             H: KT764           D: AK              C: QT6`

2. **West 2H Score: -50, EW Par: +90** (Par Contract: 2CW=)
   - *Analysis*: West's 2H overcall incurs a minor penalty (-50) when passing and defending might have resulted in plus points or a better par result.
   - *Hands*:
     - North: `S: K975            H: K3              D: 87532           C: 54`
     - West:  `S: J643            H: A98654          D: Q9              C: 9`
     - East:  `S: A82             H: T               D: 64              C: AKJT763`
     - South: `S: QT              H: QJ72            D: AKJT            C: Q82`

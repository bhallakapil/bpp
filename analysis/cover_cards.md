# Cover Cards in Bridge

Cover cards are high honors (Aces, Kings, and sometimes Queens) and other features in one hand that are expected to "cover" or neutralize losers in the partner's hand. This concept, championed by George Rosencrantz, is primarily used in suit contracts once a fit is found to evaluate game and slam potential more accurately than High Card Points (HCP).

## Definition and Valuation

Once an 8+ card fit is identified, responder evaluates their hand in terms of cover cards:

### Honor Cards
- **Ace**: 1.0 cover card.
- **King**: 1.0 cover card (except a singleton King).
- **Queen**: 
  - 1.0 cover card if in partner's bid suit.
  - 0.0 otherwise (unworthy of being a cover card in an unbid side suit).
- **Jack**: 
  - 0.5 cover card if in partner's bid suit (with a combined 8+ card fit).

### Distributional Features
Shortness covers losers in partner's side suits, provided there is adequate trump support:
- **Void**: 2.0 cover cards.
- **Singleton**: 1.0 cover card.
- **Doubleton**: Generally not counted (considered too unreliable/slow).

**Trump Length**:
- **Fourth Trump**: 0.5 cover card.

*Note: Use caution when counting shortness or slow honors (Queens/Jacks) without primary honors (Aces/Kings). The method specifically warns against double-counting distributional values and suggests downgrading "Quacker" hands.*

## Application with Losing Trick Count (LTC)

Cover cards simplify the Losing Trick Count (LTC) method for the responder. Instead of counting their own losers (which can be 9 or 10), the responder counts winners (cover cards) to subtract from the opener's expected losers.

### Basic Formula
`Expected Winners = 13 - (Opener's LTC - Responder's Cover Cards)`

### Estimating Opener's LTC
Opener's bidding provides a reliable estimate of their LTC:
- **Standard Opening (1H/1S)**: 7 LTC.
- **Help Suit Game Try (1H-2H; 3D)**: 6 LTC.
- **Strong Jump Rebid (1H-1S; 3H)**: 6 LTC.
- **Reverse (1D-1S; 2H)**: 4-5 LTC.
- **Strong Jump Shift (1H-1S; 3C)**: 4 LTC.
- **Weak 2 Preempt**: ~8 LTC.
- **3-level Preempt**: 6-7 LTC.

## Examples

### Example 1: Evaluating Game
Partner opens 1S (7 LTC). You hold:
`S: A1032 H: A2 D: A432 C: 1092` (12 HCP)
- **Cover Cards**: 1.5 (S: Ace + 4th trump) + 1.0 (H: Ace) + 1.0 (D: Ace) = **3.5**
- **Calculation**: $7 - 3.5 = 3.5$ losers remaining.
- **Result**: Since game allows 3 losers, this is a strong invitation to 4S (needs opener to be slightly better than a minimum 7 LTC).

### Example 2: Exploring Slam
Partner opens 1H, you bid 1S, partner jumps to 3C (Strong Jump Shift = 4 LTC). You hold:
`S: 10932 H: AJ2 D: 5 C: AJ92` (10 HCP)
- **Cover Cards**: 1.5 (H: AJ support) + 1.0 (D: singleton) + 2.0 (C: AJ support) = **4.5**
- **Calculation**: $4 - 4.5 = -0.5$ (Grand Slam potential).
- **Result**: Bid Blackwood / explore slam.

## LTC Recap (for reference)
Aces and Kings are not losers. Maximum 3 losers per suit.
- **Void**: 0
- **Singleton A / K**: 0 / 1
- **Doubleton AK / Ax / Kx**: 0 / 1 / 1
- **Tripleton AKx / AQx / Axx / Kxx / Qxx**: 1 / 1 / 2 / 2 / 2.5

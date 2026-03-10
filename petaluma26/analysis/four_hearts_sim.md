# 4 Hearts Simulation (South) Analysis

Simulation of the success rate for a 4 Hearts contract by South with specific constraints on North and West hands.

## Common Parameters

### North (Dummy)
- **Hearts**: Exactly 3
- **HCP**: 7 to 9

### West (Opponent)
- **HCP**: 11 to 15
- **Hearts**: 2 or fewer
- **Allowed Shapes**: 
    - 4 Spades: 4243, 4234, 4144, 4153, 4135, 4054, 4045
    - 3 Spades: 3253, 3235, 3154, 3145

## Strategy Definition
- **North 7 HCP**: Always play 3H.
- **North 8 HCP**: 50% 3H, 50% 4H.
- **North 9 HCP**: Always play 4H.

---

## Case 1: South Hand `A76 KT9543 J76 A` (HCP 12)

### Results (5,000 Trials)
| North HCP | 3H Success % | 4H Success % | Count |
|-----------|--------------|--------------|-------|
| 7         | 59.8%        | 18.9%        | 1,669 |
| 8         | 76.4%        | 31.6%        | 1,793 |
| 9         | 88.3%        | 48.6%        | 1,538 |

**Overall Strategy Success Rate: 54.3%**

---

## Case 2: South Hand `A76 KT9543 AJ7 6` (HCP 12)

### Results (5,000 Trials)
| North HCP | 3H Success % | 4H Success % | Count |
|-----------|--------------|--------------|-------|
| 7         | 75.5%        | 31.1%        | 1,710 |
| 8         | 87.5%        | 43.3%        | 1,735 |
| 9         | 95.3%        | 63.0%        | 1,555 |

**Overall Strategy Success Rate: 68.1%**

## Conclusion
Changing the South hand from Case 1 (Club Ace, Diamond Jack) to Case 2 (Diamond Ace/Jack, Club singleton) significantly improves the success rate of the 4 Hearts contract. In Case 2, 4H is a solid 63.0% favorite with 9 HCP partner, compared to only 48.6% in Case 1.

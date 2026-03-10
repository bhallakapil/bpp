# Simulation Summary: 3NT by East (3NE)

**Total Samples:** 100 deals

## Conditions
- **South Hand (Leader):** `♠AJ10953 ♥J1073 ♦103 ♣4`
- **East (Declarer):** 20-21 HCP. Shapes: Balanced (4333, 4432, 5332) or Semi-balanced with 6-card minor (6322). Excludes 5-4 major distributions.
- **West (Dummy):** 5-7 HCP, ≤ 3 Spades, ≤ 3 Hearts.

## Statistical Results
| Lead Choice | Avg. Tricks for Declarer | Contract Failure Rate (East < 9 tricks) |
| :--- | :--- | :--- |
| **SJ Lead** | **9.63** | **24.0%** |
| **Non-Spade Lead** | **9.67** | **20.8%** |

## Conclusion
Leading the **Jack of Spades (SJ)** is the superior defensive strategy for South. In this sample of 100 deals, it results in a higher failure rate (**24.0%**) for declarer compared to non-spade leads (**20.8%**).

---

## SJ Lead vs Specific Alternatives with Expanded East Shapes (5000 Samples)

**Total Samples:** 5000 deals

### Conditions
- **South Hand (Leader):** `♠AJ10953 ♥J1073 ♦103 ♣4`
- **East (Declarer):** 20-21 HCP. Shapes: Balanced (4333, 4432, 5332), Semi-balanced (6322), or **2245 / 2254**. Excludes 5-4 major distributions.
- **West (Dummy):** 3-12 HCP. Shapes: ≤ 3 in majors OR (4333) OR (3433).

### Statistical Results
| Lead Choice | SJ More Tricks | SJ Same Tricks | SJ Less Tricks |
| :--- | :---: | :---: | :---: |
| **vs Heart 3 (H3)** | 1579 | 2048 | 1373 |
| **vs Diamond Ten (DT)** | 1441 | 2110 | 1449 |
| **vs Club 4 (C4)** | 1406 | 2142 | 1452 |

### Analysis
With the inclusion of East hands with 2245 and 2254 distributions, the Jack of Spades (SJ) lead continues to be a strong option, particularly against the Heart 3 (H3) lead. Against the minor suits (DT and C4), the results are very close, with SJ being slightly less effective than the alternative leads in a small percentage of cases.

---

## Refined West Hand Constraints (10,000 Samples)

**Total Samples:** 10,000 deals

### Conditions
- **South Hand (Leader):** `♠AJ10953 ♥J1073 ♦103 ♣4`
- **East (Declarer):** 20-21 HCP. Shapes: Balanced (4333, 4432, 5332), Semi-balanced (6322), or **2245 / 2254**. Excludes 5-4 major distributions.
- **West (Dummy):** 3-12 HCP. Shapes: 
    - ≤ 3 in both majors OR exactly (4333) / (3433).
    - **No Voids** in any suit.
    - **Max Suit Length:** 6 cards.
    - **Two Longest Suits:** Sum ≤ 9 cards.

### Statistical Results
| Lead Choice | SJ More Tricks | SJ Same Tricks | SJ Less Tricks |
| :--- | :---: | :---: | :---: |
| **vs Heart 3 (H3)** | 3164 | 4313 | 2523 |
| **vs Diamond Ten (DT)** | 2847 | 4489 | 2664 |
| **vs Club 4 (C4)** | 2748 | 4589 | 2663 |

### Analysis
With a larger sample size (10,000 deals) and restrictive West hand shapes, the Jack of Spades (SJ) lead consistently outperforms the alternatives. It is better than H3 in 31.6% of cases, better than DT in 28.5%, and better than C4 in 27.5%. Across all comparisons, the SJ lead is superior to or equal to alternative leads in approximately 73-75% of deals.

---

## Dual Scoring Comparison: IMPs vs Matchpoints

**Total Samples:** 4,400 deals (Simulation of 10,000 intended)

### Conditions
- **South Hand (Leader):** `♠AJ10953 ♥J1073 ♦103 ♣4`
- **East (Declarer):** 20-21 HCP. Shapes: Balanced (4333, 4432, 5332), Semi-balanced (6322), or 2245 / 2254. Excludes 5-4 major distributions.
- **West (Dummy):** 3-12 HCP. Refined shapes as per previous 10,000 sample run.

### Statistical Results (Payoff Comparison)

#### IMPs (Average IMP gain for row lead vs column lead)
| Lead | vs ♠A | vs ♥J | vs ♦T | vs ♣4 |
| :--- | :---: | :---: | :---: | :---: |
| **♠J** | +1.28 | +0.52 | +0.98 | +1.04 |
| **♥J** | +0.75 | - | +0.48 | +0.54 |

#### Matchpoints (Pairwise victory probability for row lead vs column lead)
| Lead | vs ♠A | vs ♠J | vs ♦T | vs ♣4 |
| :--- | :---: | :---: | :---: | :---: |
| **♥J** | +0.31 | +0.13 | +0.14 | +0.14 |
| **♠J** | +0.20 | - | -0.03 | -0.03 |

### Analysis
The results highlight a significant divergence in strategy between scoring formats:
- **In IMPs**, the **Jack of Spades (♠J)** is clearly superior. It maximizes the chance of a large defensive gain (defeating the contract), which is rewarded heavily in IMP scoring.
- **In Matchpoints**, the **Jack of Hearts (♥J)** becomes the better choice. It is a more passive, "safe" lead that protects against giving away unnecessary overtricks, which is crucial for preserving a good score in pair games.

---

*Simulation performed using `redeal` and DDS. Simulation scripts: [`petaluma26/sj_lead_sim.py`](petaluma26/sj_lead_sim.py), [`petaluma26/sj_opening_lead_sim.py`](petaluma26/sj_opening_lead_sim.py)*

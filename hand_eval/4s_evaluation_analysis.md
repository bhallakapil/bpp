# 4S Contract Evaluation Analysis

**Scenario:**
- **South Hand:** `♠ AQ853 ♥ T82 ♦ A ♣ AQ52` (16 HCP, 5-3-1-4)
- **North Hand:** 5-9 HCP, holding 3+ spades (with side singletons allowed for 3-card spade support, but excluded for 4+ spade support).
- **Simulation Sample Size:** 10,000 deals (double-dummy analysis).

---

## Overall Results

- **Overall 4S Success Rate:** **59.34%** (5,934 / 10,000 makes)

---

## North Spade Length Percentages

- **3 Spades:** 6,469 / 10,000 (**64.69%**)
- **4 Spades:** 2,666 / 10,000 (**26.66%**)
- **5+ Spades:** 865 / 10,000 (**8.65%**)

---

## Detailed Matrices (HCP vs Singleton Status)

### 1. 3 Spades Holding

| HCP | With Singleton (Makes / Total, %) | Without Singleton (Makes / Total, %) |
| :--- | :--- | :--- |
| **5** | 90/201 (44.8%) | 146/863 (16.9%) |
| **6** | 117/236 (49.6%) | 289/996 (29.0%) |
| **7** | 199/277 (71.8%) | 502/1184 (42.4%) |
| **8** | 212/264 (80.3%) | 718/1170 (61.4%) |
| **9** | 214/249 (85.9%) | 781/1029 (75.9%) |

### 2. 4 Spades Holding

| HCP | With Singleton (Makes / Total, %) | Without Singleton (Makes / Total, %) |
| :--- | :--- | :--- |
| **5** | 0/0 (0.0%) | 183/397 (46.1%) |
| **6** | 0/0 (0.0%) | 327/522 (62.6%) |
| **7** | 0/0 (0.0%) | 436/604 (72.2%) |
| **8** | 0/0 (0.0%) | 490/600 (81.7%) |
| **9** | 0/0 (0.0%) | 492/543 (90.6%) |

### 3. 5+ Spades Holding

| HCP | With Singleton (Makes / Total, %) | Without Singleton (Makes / Total, %) |
| :--- | :--- | :--- |
| **5** | 0/0 (0.0%) | 121/161 (75.2%) |
| **6** | 0/0 (0.0%) | 144/178 (80.9%) |
| **7** | 0/0 (0.0%) | 169/198 (85.4%) |
| **8** | 0/0 (0.0%) | 164/182 (90.1%) |
| **9** | 0/0 (0.0%) | 140/146 (95.9%) |

---

## Strategic Summary

1. **Fit & Shape Impact:** Side singletons with 3-card spade support significantly enhance contract performance at lower and upper HCP ranges.
2. **Trump Length Distribution:** 3-card spade support constitutes the majority of valid North responses (64.69%), followed by 4-card support (26.66%) and 5+ card support (8.65%).
3. **Longer Trumps:** 5+ spade holdings without singletons show robust success rates across all HCP levels (75.2% to 95.9%).

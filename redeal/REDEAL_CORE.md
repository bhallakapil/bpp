# `redeal/redeal.py` - Core Library Documentation

This document provides a detailed technical analysis of the classes and logic within [`redeal/redeal.py`](redeal.py).

## 1. Class Overview

| Class | Base Class | Description |
| :--- | :--- | :--- |
| `Shape` | `object` | Handles suit distribution patterns and filtering (e.g., balanced hands). |
| `Evaluator` | `object` | Provides additive scoring for holdings (HCP, QP, Controls). |
| `Hand` | `tuple` | Represents a single bridge hand of 13 cards across four suits. |
| `Deal` | `tuple` | A collection of four `Hand` objects representing a full bridge deal. |
| `Holding` | `frozenset` | Represents a single-suit holding (e.g., the Spades in a hand). |
| `Contract` | `object` | The "Rulebook": Defines scoring logic for a specific bid and result. |
| `ScoredContract`| `object` | The "Scoreboard": Associates a contract with a declarer and net result. |
| `Simulation` | `object` | Base class for orchestrating simulation lifecycles. |
| `Payoff` | `object` | Statistical utility for comparing lead or play strategies. |

---

## 2. Part I: Foundation & Configuration

The foundation of any simulation involves defining what hands to accept (`Shape`) and how to value them (`Evaluator`).

### `Shape`
An immutable specification for suit distributions.
- **The 560 Combinations**: In bridge, there are exactly **560 unique distributions** of 13 cards across four suits (e.g., 4-4-3-2, 5-3-3-2). The `Shape` class pre-calculates every possible combination in its `_all_shapes` attribute. 
    - *See the full list in [`redeal/SHAPES.md`](SHAPES.md).*
- **Bit-Table Optimization**: Pre-calculates these 560 shapes into an `array("b")`. This allows for extremely fast $O(1)$ lookup for hand distributions (e.g., `hand.shape in balanced`).
- **Initialization & Parsing**:
    - **String Parsing**: `Shape("(4432)")` accepts any permutation of 4-4-3-2. wildcards like `Shape("55xx")` are also supported.
    - **Functional Conditions**: `Shape.from_cond(lambda s,h,d,c: s >= 5)` allows for programmatic shape definition.
- **Set Operations**: Supports `+` (union) and `-` (difference) to build complex shapes.
    - *Example*: `semibalanced = balanced + Shape("(5422)") + Shape("(6322)")`.
- **Caching**: Uses an internal `_cls_cache` to ensure that identical shape strings return the same object, saving memory and time during large simulations.
- **SmartStack Integration**: Tracks `min_ls` and `max_ls` (min/max suit lengths) for each suit, providing optimization hints to the deal generator.

### `Evaluator`
A generic tool for performing additive hand evaluations by assigning weights to ranks.
- **Rank Mapping**: When initialized with `Evaluator(4, 3, 2, 1)`, it assigns 4 to Ace (rank 14), 3 to King (rank 13), etc. Any ranks not specified are assigned a value of 0.
- **Recursive Calling**:
    - **Holding**: Sums the values for each rank present in the suit.
    - **Hand**: Iterates over all four suits and returns the total sum.
- **Example (Cover Cards)**: You can define custom metrics like "Cover Cards" (Ace=1, King=1, Queen=0.5):
    ```python
    cover_cards = Evaluator(1, 1, 0.5)
    print(cover_cards(hand))
    ```

---

## 3. Part II: Data Models & Generation

These classes represent the physical state of the bridge table and provide high-level analysis tools.

### `Deal`
A collection of four `Hand` objects.
- **Dealer Factory**: `Deal.prepare(predeal)` creates a generator that respects fixed cards. It can handle `SmartStack` objects for one seat to avoid rejection sampling.
- **Generation Loop**: `Deal(dealer, tries=1000)` will repeatedly attempt to generate a deal that satisfies a given `accept_func`.
- **Double Dummy Analysis**: Integrates with the `dds` library.
    - **`dd_tricks(contract)`**: Computes max tricks. Uses an internal `_dd_cache` to avoid redundant DDS calls for the same strain/declarer.
    - **`dd_all_tricks(strain, leader)`**: Returns a dictionary mapping every valid lead card to the resulting trick count for the declarer.
    - **`par(dealer, nsvul, ewvul)`**: Exhaustively searches the contract space to find the optimal result for both sides.

### `Hand`
A tuple of four `Holding` objects.
- **Evaluation Aggregation**: Provides lazy-calculated (reified) properties for `hcp`, `qp`, `controls`, `losers`, `newltc`, and `pt`.
- **Distribution Metrics**:
    - **`l1`, `l2`, `l3`, `l4`**: The lengths of the hand's suits sorted from longest to shortest.
    - **`freakness`**: Pavlicek's freakness score, calculated as `sum(max(l-4, 3-l)) + adjustment` for short suits.
- **Suit Access**: Convenience properties `spades`, `hearts`, `diamonds`, `clubs`.

### `Holding`
A `frozenset` of card ranks within a single suit.
- **LTC (Loser Trick Count)**:
    - **`losers`**: Traditional count (max 3 per suit). Missing A, K, or Q in a 3+ card suit counts as 1 loser each.
    - **`newltc`**: Fractional weights (Ace=1.5, King=1.0, Queen=0.5) for more precise evaluation.
- **Pavlicek Playing Tricks (`pt`)**: 
    Uses a detailed lookup for honor combinations (e.g., `AKJ` = 2.5 tricks) and adds 1 trick for every card beyond the 3rd.

---

## 4. Part III: Simulation Framework

The framework that drives the generation and processing of deals.

### `Simulation`
Defines the lifecycle methods for a simulation:
- **`initial(self)`**: Called once. Ideal for setting up trackers or `Payoff` tables.
- **`accept(self, deal)`**: A filter returning `True` if the deal should be included in the results.
- **`do(self, deal)`**: The core logic (e.g., printing or scoring) performed on accepted deals.
- **`final(self, n_tries)`**: Post-simulation reporting, such as calculating averages or printing tables.

```mermaid
graph TD
    Start((Start)) --> Initial[initial()]
    Initial --> GenDeal[Generate Deal]
    GenDeal --> Accept{accept?}
    Accept -- No --> GenDeal
    Accept -- Yes --> Do[do()]
    Do --> Count{Target Count Reached?}
    Count -- No --> GenDeal
    Count -- Yes --> Final[final()]
    Final --> End((End))
```

### `OpeningLeadSim`
A specialized `Simulation` that:
1. Identifies valid leads for the defending side.
2. Compares them using a `Payoff` table.
3. Automatically handles contract and declarer setup.

### `Payoff`
A statistical engine that tracks **pairwise differences**. Instead of comparing absolute scores, it calculates `score(A) - score(B)` for every deal, allowing it to determine if Strategy A is statistically better than Strategy B even with a small sample size.
- **Reporting**: Displays mean differences and standard errors.
- **Formatting**: Uses colorama to highlight results (Bright Green for statistically significant gains).

---

## 5. Part IV: Scoring & Statistics

### `Contract` (The Rules)
Implements the full WBF scoring table via the `score(tricks)` method.
- **Trick Points**: 20 (Minors), 30 (Majors), 40/30 (NT).
- **Game/Slam Bonuses**:
    - **Game**: 300 (non-vul), 500 (vul).
    - **Small Slam**: 500 (non-vul), 750 (vul).
    - **Grand Slam**: 1000 (non-vul), 1500 (vul).
- **Doubling**: Multiplies trick points and adds an "insult" bonus (50 for X, 100 for XX).
- **Undertricks**: Calculates penalties based on vulnerability and doubling status.

### `ScoredContract` (The Result)
A container for a `Contract`, `declarer`, and `tricks`.
- **Net Perspective**: Automatically calculates the score from the **North-South (NS)** point of view.
- **Output**: Formats results like `3NS+1 (+430)` for making a contract or `4HW-2 (+100)` for setting the opponents.

### Scoring Functions
- **[`imps(my, other)`](redeal.py:691)**: Optimized range-lookup using binary search (`bisect`) against the official 0-24 IMP threshold table.
- **[`matchpoints(my, other)`](redeal.py:686)**: Standard pairwise victory comparison (+1 for win, -1 for loss, 0 for tie).

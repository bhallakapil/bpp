# Redeal - A Bridge Simulation Library

Redeal is a Python implementation of the "Deal" bridge hand generator, designed for high-performance simulation and analysis.

## File Overview

| File | Functionality |
| :--- | :--- |
| `__init__.py` | Package initialization; exposes version and core functionality. |
| `__main__.py` | Command-line interface entry point; handles argument parsing and script execution. |
| `bigdeal.py` | Pure Python implementation of the "bigdeal" algorithm for board generation and hand mapping. |
| `dds.py` | Python interface to the Double Dummy Solver (DDS) library. |
| `global_defs.py` | Core bridge constants and enums (Seat, Suit, Strain, Rank, Card). |
| `redeal.py` | Main library file containing core logic (Hand, Deal, Contract, Simulation). |
| `smartstack.py` | Specialized dealer for efficient generation of constrained hands. |
| `util.py` | Internal utilities for dynamic code and lazy properties. |

## Core Utilities

### `reify` (Lazy Property)
A performance optimization decorator that calculates a value (like HCP) only once, upon first access, and then replaces itself with the calculated value. This significantly speeds up simulations that access the same property multiple times per hand.

### `create_func`
Dynamically generates Python functions from strings at runtime, allowing users to provide custom simulation logic (like `accept` or `do`) via the command line or script files.

## SmartStack
`SmartStack` is an advanced hand generator that avoids the slow "rejection sampling" method. Instead of generating a random hand and checking if it fits, it pre-calculates valid patterns that satisfy specific shape and point-count constraints.

1. **Pre-calculation:** Groups all possible 1-suit holdings by `(length, value)`.
2. **Pattern Discovery:** Finds all valid combinations of 4-suit patterns that meet the total 13-card and evaluation criteria.
3. **Probability Mapping:** Weights each pattern based on its mathematical frequency.
4. **Instant Generation:** When called, it picks a valid pattern and then selects random holdings for each suit to build the hand.

**Usage:** `SmartStack` is used whenever a simulation script provides one for a seat (e.g., North) within the `predeal` dictionary. When the `Main` loop requests a deal, `SmartStack` generates the constrained hand first, and the remaining 39 cards are then dealt to the other seats.

## Hand Generation (Big Deal)
Redeal uses a pure Python implementation of the industry-standard "bigdeal" algorithm for high-quality, cryptographically secure randomness:

- **Entropy Collection**: Handles entropy collection (`os.urandom`) and seed generation. It uses RIPEMD-160 hashing to produce a 96-bit "Goedel number"—a unique index representing one of the $5.36 \times 10^{28}$ possible bridge deals.
- **Hand Mapping**: Provides the mapping logic that transforms the Goedel number into a full bridge deal. It uses combinatorial mathematics (`math.comb`) to select 13 cards for each seat in a deterministic, reproducible way.

## Double Dummy Solver (DDS)
The `dds.py` file provides a Python wrapper (via `ctypes`) for the high-performance C++ Double Dummy Solver library. It allows you to solve bridge boards from within Python:

- **`solve()`**: Returns the maximum number of tricks a declarer can take.
- **`solve_all()`**: Returns the number of tricks for every possible lead card, allowing for lead analysis.
- **`valid_cards()`**: Identifies all legally playable cards in a given situation.
- **Dynamic Loading**: Automatically loads the correct shared library (`libdds.so` on Linux/macOS or `dds.dll` on Windows).

## Simulation Framework (`__main__.py`)
The `__main__.py` file orchestrates the entire simulation process via the `Main` class:

- **Argument Parsing:** Uses `argparse` to handle CLI arguments and `runpy` to load user-provided scripts. Command-line flags (like `-N` or `--accept`) have higher priority than settings within a script.
- **Simulation Object:** Prepares a `Simulation` instance. If a script provides one, it is used; otherwise, a custom `Simulation` class is created dynamically using `create_func`.
- **Generation Loop (`Main.generate`):**
    1. Prepares a `Dealer` (incorporating any `SmartStack` from `predeal`).
    2. Runs the simulation's `initial()` function.
    3. Repeatedly generates deals and checks them against `simulation.accept()`.
    4. When a deal is accepted, it increments the count and runs `simulation.do(deal)`.
    5. Stops once the requested number of deals (`-n`) is found or the maximum number of attempts (`--max`) is reached.
    6. Runs the simulation's `final()` function.

## Command Line Usage

### General Options
- `-n`: Number of deals to generate (default: 10).
- `-f, --format`: Output style (`short`, `long`, or `pbn`).
- `-o, --only`: Hands to print (e.g., `NESW`).
- `-v, --verbose`: Show progress during generation.
- `--gui`: Starts the graphical interface.

### Script Overrides
- `-N, -E, -S, -W`: Specify pre-dealt hands for a seat.
- `--accept`: Define custom acceptance logic via CLI string.
- `--do`: Define custom action logic via CLI string.
- `--initial`: Define custom initialization logic.
- `--final`: Define custom final summary logic.

# TDMA Schedule Planner and Optimizer

A Python-based simulator for planning TDMA (Time Division Multiple
Access) transmission schedules in a wireless network.

The project models wireless radios as graph nodes and communication
relationships as graph edges. It then constructs a Distance-2 conflict
graph and uses graph-coloring heuristics to generate a conflict-free
TDMA schedule.

---

## 1. Project Objective

The objective of this project is to design a centralized schedule
planner for a TDMA-based wireless network.

The optimizer:

- Accepts coordinates of 16 wireless nodes.
- Builds a wireless connectivity graph.
- Uses a 500-meter communication range.
- Identifies 1-hop and 2-hop interference relationships.
- Constructs a Distance-2 conflict graph.
- Uses graph-coloring heuristics for slot assignment.
- Allows spatial reuse of TDMA slots when nodes are sufficiently
  separated in the conflict graph.
- Validates the generated schedule.
- Produces a Slot × Node boolean matrix.
- Exports the generated schedule as JSON and CSV.

---

## 2. Problem Model

Each wireless radio is represented as a node in a graph.

An edge is created between two nodes when their Euclidean distance
is less than or equal to 500 meters.

The resulting graph represents wireless connectivity.

For TDMA scheduling, simply preventing direct neighbors from sharing
a slot is insufficient.

The implementation therefore uses Distance-2 graph coloring.

Two nodes are considered conflicting when their shortest-path distance
in the wireless graph is:

- 1 hop
- 2 hops

Nodes more than 2 hops apart are allowed to reuse the same slot.

---

## 3. System Architecture

The overall processing pipeline is:

    Node Coordinates
           |
           v
    Input Validation
           |
           v
    Wireless Network Graph
           |
           v
    Distance-2 Conflict Graph
           |
           v
    Graph Coloring Optimizer
           |
           v
    TDMA Slot Assignment
           |
           v
    Schedule Validation
           |
           v
    Slot × Node Matrix
           |
           +------------------+
           |                  |
           v                  v
      schedule.json      schedule.csv

---

## 4. Graph Construction

The wireless network is represented using NetworkX.

For every pair of nodes:

    distance = sqrt((x2-x1)^2 + (y2-y1)^2)

If:

    distance <= 500 meters

an edge is created between the two nodes.

The graph therefore represents the physical communication
relationships between radios.

---

## 5. Distance-2 Conflict Graph

The wireless connectivity graph is transformed into a conflict graph.

For every pair of nodes, the shortest-path distance is calculated.

A conflict edge is created when:

    shortest_path_distance <= 2

Therefore:

    1-hop relationship → conflict
    2-hop relationship → conflict
    >2-hop relationship → possible spatial reuse

The conflict graph is then used as the input to the coloring algorithm.

---

## 6. TDMA Slot Assignment

The scheduling problem is represented as a graph-coloring problem.

Each color represents a TDMA time slot.

Therefore:

    Graph Node → Wireless Radio
    Graph Edge → Scheduling Conflict
    Graph Color → TDMA Slot

The optimizer evaluates multiple coloring strategies.

### Strategies

1. Largest First
2. Smallest Last
3. DSATUR
4. 100 deterministic randomized greedy colorings

Each candidate coloring is evaluated according to the number of
TDMA slots used.

The candidate using the fewest slots is selected.

The randomized candidates use fixed seeds so that the optimization
process is reproducible.

---

## 7. Why Multiple Heuristics?

The exact minimum graph-coloring problem is computationally difficult
for general graphs.

Instead of relying on a single greedy ordering, this project evaluates
multiple heuristics.

This provides several candidate schedules and selects the candidate
with the smallest number of slots.

The result is therefore a heuristic solution rather than a mathematical
proof of the minimum possible number of slots.

---

## 8. Schedule Validation

After coloring, every pair of nodes connected in the conflict graph
is checked.

A schedule is considered valid when:

    conflict_node_A.slot != conflict_node_B.slot

for every conflict edge.

If any conflicting nodes share a slot, the schedule is reported as
invalid.

---

## 9. Schedule Matrix

The optimizer generates a Slot × Node matrix.

The matrix uses:

    1 → Node transmits in that slot
    0 → Node does not transmit in that slot

Example:

    Slot     Node_01  Node_02  Node_03
    Slot 0      1        0        1
    Slot 1      0        1        0

This representation can be used as the basis for a TDMA schedule
planner or a later simulation interface.

---

## 10. CLI Usage

Run the optimizer from the project root using:

    python src/main.py --input examples/nodes.json

A different topology can be supplied using another JSON file:

    python src/main.py --input examples/my_network.json

The output directory can also be specified:

    python src/main.py \
        --input examples/nodes.json \
        --output-dir outputs

---

## 11. Input Format

The input JSON contains node names and their [x, y] coordinates.

Example:

    {
        "Node_01": [0.0, 0.0],
        "Node_02": [300.0, 0.0],
        "Node_03": [900.0, 0.0]
    }

The current implementation expects exactly 16 nodes for the
assignment.

Input validation checks:

- JSON must contain an object.
- Exactly 16 nodes must be provided.
- Each node must contain two coordinates.
- Coordinates must be numeric.

---

## 12. Output

The optimizer produces:

### schedule.json

Contains:

- Total number of slots
- Schedule validation result
- Node-to-slot assignments

### schedule.csv

Contains the Slot × Node boolean matrix.

---

## 13. Example Run

For the current 16-node test topology:

    Total nodes: 16
    Wireless links: 27
    Conflict links: 53

The optimizer evaluates:

    103 coloring strategies

The selected coloring currently produces:

    7 TDMA slots

The generated schedule is validated successfully:

    VALID: No conflicting nodes share the same TDMA slot.

Note that the 7-slot result is a heuristic coloring result and is not
claimed to be the mathematically minimum coloring.

---

## 14. Project Structure

    tdma-schedule-optimizer/
    |
    +-- docs/
    |
    +-- examples/
    |   +-- nodes.json
    |
    +-- outputs/
    |   +-- schedule.json
    |   +-- schedule.csv
    |
    +-- src/
    |   +-- graph.py
    |   +-- scheduler.py
    |   +-- main.py
    |
    +-- tests/
    |   +-- test_scheduler.py
    |
    +-- .gitignore
    +-- README.md
    +-- requirements.txt

---

## 15. Testing

The project uses pytest for automated testing.

Run:

    python -m pytest

Current test coverage includes:

- Wireless graph construction
- Wireless connectivity validation
- Conflict graph construction
- Schedule conflict validation
- Schedule matrix generation
- Node slot assignment
- Non-negative slot validation
- Invalid node-count handling
- Invalid coordinate handling
- Non-numeric coordinate handling

Current result:

    9 passed

---

## 16. Technology Stack

- Python
- NetworkX
- Pytest
- Graph Theory
- TDMA Scheduling
- Distance-2 Graph Coloring
- JSON
- CSV

---

## 17. Current Status

### Part 1 — Centralized TDMA Optimizer

Status: Implemented

The current implementation supports:

- 16-node JSON input
- 500-meter connectivity modeling
- Distance-2 conflict detection
- Multiple graph-coloring heuristics
- Schedule validation
- Slot × Node matrix generation
- JSON output
- CSV output
- CLI execution
- Automated testing

### Part 2 — EMANE Integration

Status: Planned

Future work includes investigating:

- EMANE environment setup
- TDMA Radio Model configuration
- Schedule-to-XML/ProtoBuf conversion
- Integration of the generated schedule with a network simulation

---

## 18. Future Improvements

Potential improvements include:

- Additional topology input formats
- More advanced graph-coloring heuristics
- Performance benchmarking
- Visualization of the wireless topology
- Visualization of the conflict graph
- EMANE integration
- Schedule export for a real TDMA radio model
- Simulation-based evaluation
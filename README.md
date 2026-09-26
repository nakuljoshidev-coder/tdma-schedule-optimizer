# TDMA Schedule Planner and Optimizer

A centralized Python-based TDMA (Time Division Multiple Access) Schedule Planner and Optimizer developed for the Vaan Megam Networks Wireless Protocol Development Internship assignment.

The project models a wireless network as a graph, constructs a Distance-2 conflict graph, and uses graph-coloring heuristics to generate a conflict-free TDMA schedule with spatial slot reuse.

---

## Overview

In a TDMA-based wireless network, radios transmit during assigned time slots. Nearby radios cannot transmit simultaneously when they may interfere with each other.

This project solves the scheduling problem by:

- Representing radios as graph nodes.
- Creating wireless links between nodes within 500 meters.
- Constructing a Distance-2 conflict graph.
- Preventing conflicting nodes from sharing the same TDMA slot.
- Applying multiple graph-coloring heuristics.
- Selecting the best heuristic schedule found.
- Validating the generated schedule.
- Exporting the schedule as JSON and CSV.
- Generating a visualization of the network topology.

---

## Key Features

- 500-meter wireless communication range
- Distance-2 conflict graph construction
- TDMA slot assignment
- Spatial reuse of TDMA slots
- Multiple graph-coloring strategies
- Randomized greedy optimization
- Automatic schedule validation
- JSON input support
- JSON and CSV schedule output
- Slot × Node Boolean matrix
- Node → Slot mapping
- Network topology visualization
- Automated test suite
- Command-line interface

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3 | Core implementation |
| NetworkX | Graph construction and algorithms |
| Pytest | Automated testing |
| Matplotlib | Network visualization |
| JSON | Node coordinate input |
| CSV | Schedule export |

---

## System Architecture

Node Coordinates
        |
        v
Wireless Network Graph
        |
    500 m Range
        |
        v
Distance-2 Conflict Graph
        |
        v
Graph Coloring Algorithms
        |
        +----------------+
        |                |
        v                v
Largest First       Smallest Last
        |                |
        +-------+--------+
                |
                v
             DSATUR
                |
                v
      Randomized Greedy
          100 Trials
                |
                v
        Best Candidate
                |
                v
       TDMA Slot Assignment
                |
        +-------+-------+
        |       |       |
        v       v       v
      JSON    CSV   Visualization
                |
                v
       Schedule Validation

---

## Wireless Network Model

Each wireless radio is represented as a node in the network graph.

Two nodes are connected when their Euclidean distance is less than or equal to 500 meters.

The distance is calculated using:

d = sqrt((x2 - x1)^2 + (y2 - y1)^2)

A communication link exists when:

d <= 500 meters

---

## Distance-2 Conflict Model

The wireless network graph is converted into a Distance-2 conflict graph.

Two nodes are considered conflicting when their shortest-path distance is:

- 1 hop
- 2 hops

Therefore:

1-hop nodes  -> conflict
2-hop nodes  -> conflict
3+ hop nodes -> may reuse a slot

This allows spatial reuse while ensuring that nodes within the required interference range do not transmit during the same TDMA slot.

---

## TDMA Slot Assignment

The TDMA scheduling problem is treated as a graph-coloring problem.

Graph Node  -> Wireless Radio
Graph Color -> TDMA Slot
Graph Edge  -> Scheduling Conflict

The optimizer evaluates multiple coloring strategies:

1. Largest First
2. Smallest Last
3. DSATUR / Saturation Largest First
4. 100 randomized greedy orderings

The candidate using the fewest slots among the evaluated schedules is selected.

The result is a heuristic solution and is not claimed to be the mathematically optimal coloring.

---

## Input Format

The optimizer accepts a JSON file containing node names and their [x, y] coordinates.

Example:

{
    "Node_01": [0.0, 0.0],
    "Node_02": [300.0, 0.0],
    "Node_03": [900.0, 0.0],
    "Node_04": [900.0, 300.0]
}

The supplied example contains 16 wireless nodes.

---

## Project Structure

tdma-schedule-optimizer/
|
+-- docs/
|   +-- VMN_TDMA_Technical_Documentation.pdf
|   +-- VMN_TDMA_Schedule_Optimizer_Presentation.pptx
|
+-- examples/
|   +-- nodes.json
|
+-- outputs/
|   +-- schedule.json
|   +-- schedule.csv
|   +-- network_topology.png
|
+-- src/
|   +-- graph.py
|   +-- main.py
|   +-- scheduler.py
|   +-- visualize.py
|
+-- tests/
|   +-- test_scheduler.py
|
+-- .gitignore
+-- README.md
+-- requirements.txt

---

## Installation

Clone the repository:

git clone https://github.com/nakuljoshidev-coder/tdma-schedule-optimizer.git

cd tdma-schedule-optimizer

Create a virtual environment:

python -m venv .venv

Activate it on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

---

## Running the Optimizer

Run the centralized TDMA optimizer using:

python src/main.py --input examples/nodes.json

The program:

1. Loads the node coordinates.
2. Validates the input.
3. Builds the wireless network graph.
4. Builds the Distance-2 conflict graph.
5. Runs multiple coloring strategies.
6. Selects the best heuristic result.
7. Validates the schedule.
8. Generates the schedule matrix.
9. Exports JSON and CSV results.

---

## Example Result

For the supplied 16-node topology, the optimizer currently produces:

Nodes:             16
Wireless Links:    27
Conflict Links:    53
TDMA Slots:        7
Schedule:          VALID

The generated schedule is conflict-free according to the Distance-2 conflict graph.

The seven-slot result is a heuristic result for this topology and is not claimed to be the global minimum.

---

## Node-to-Slot Assignment

The optimizer generates a mapping in the following form:

Node_01 -> Slot 0
Node_02 -> Slot 1
Node_03 -> Slot 0
Node_04 -> Slot 3
...

This mapping is also stored in the generated JSON output.

---

## Schedule Matrix

The optimizer generates a Slot × Node Boolean matrix.

1 = Node transmits during the slot
0 = Node does not transmit during the slot

Example:

          Node_01  Node_02  Node_03
Slot 0       1        0        1
Slot 1       0        1        0
Slot 2       0        0        0

---

## Schedule Validation

After slot assignment, every edge in the Distance-2 conflict graph is checked.

For every pair of conflicting nodes:

slot(Node_A) != slot(Node_B)

must be true.

The program reports:

VALID: No conflicting nodes share the same TDMA slot.

when the schedule passes validation.

---

## Generated Files

### schedule.json

Contains:

- Node coordinates
- Network statistics
- Node-to-slot assignments
- Schedule matrix
- Validation result
- Total number of slots

### schedule.csv

Contains the Slot × Node Boolean schedule in tabular form.

### network_topology.png

Contains a visual representation of:

- Node positions
- Wireless links
- TDMA slot assignments
- Network statistics

---

## Network Visualization

The visualization can be generated with:

python src/visualize.py

The resulting image is saved to:

outputs/network_topology.png

---

## Testing

The project includes an automated Pytest suite.

Run:

python -m pytest

Current test suite:

9 passed

The tests cover:

- Wireless graph construction
- Distance-2 conflict graph construction
- Schedule validation
- Schedule matrix generation
- Node slot assignment
- Non-negative slot values
- Node-count validation
- Coordinate validation
- Non-numeric coordinate validation

---

## Optimization Strategy

The optimizer uses multiple graph-coloring approaches rather than relying on a single greedy ordering.

The evaluated strategies are:

1. Largest First
2. Smallest Last
3. DSATUR / Saturation Largest First
4. 100 randomized greedy orderings

The resulting candidate schedules are compared by the number of TDMA slots used, and the candidate with the smallest slot count is selected.

Because graph coloring is computationally difficult in the general case, this implementation uses heuristic optimization rather than claiming an exact globally optimal solution.

---

## Complexity

Wireless graph construction examines pairs of nodes and therefore has quadratic pairwise behavior with respect to the number of nodes.

The Distance-2 conflict graph is constructed using shortest-path calculations.

Graph coloring is performed using heuristic algorithms rather than an exact minimum-color solver.

This approach provides a practical scheduling solution while avoiding the computational cost of solving the general graph-coloring problem exactly.

---

## Engineering Decisions

### Why NetworkX?

NetworkX provides a convenient representation of wireless networks as graphs and provides graph algorithms required for coloring and shortest-path analysis.

### Why Distance-2 Coloring?

The assignment requires nodes that are directly connected or share a common neighbor to use different slots.

Distance-2 graph coloring directly represents this constraint.

### Why Multiple Heuristics?

Different greedy coloring strategies can produce different numbers of colors depending on node ordering.

Testing several strategies increases the opportunity to find a lower-slot schedule without requiring an exact graph-coloring solver.

### Why Randomized Greedy?

Random node orderings can produce different valid colorings.

Running multiple randomized trials provides additional candidate schedules that can be compared.

---

## Limitations

- The optimizer uses heuristic graph coloring.
- The selected number of slots is not guaranteed to be globally optimal.
- The current interference model is based on Distance-2 graph constraints.
- Detailed physical-layer effects such as SINR and propagation characteristics are not currently modeled.
- The current optimizer is centralized.
- EMANE integration is not part of the implemented Part 1 optimizer.

---

## Part 1 Status

COMPLETED

The centralized Python TDMA Schedule Planner and Optimizer implements the core Part 1 requirements:

- Static node coordinates
- 500-meter communication range
- Network graph
- Distance-2 conflict graph
- TDMA slot assignment
- Spatial reuse
- Schedule validation
- Slot × Node matrix
- Node-to-slot mapping
- JSON input
- JSON and CSV output
- CLI
- Automated tests

---

## Part 2 — EMANE Integration

The assignment also includes an advanced EMANE-based extension.

The planned architecture is:

Python TDMA Optimizer
        |
        v
Generated TDMA Schedule
        |
        v
Schedule Conversion / Bridge
        |
        v
EMANE TDMA Radio Model
        |
        v
Wireless Network Simulation

The current project documents the EMANE integration approach separately from the completed centralized Part 1 implementation.

---

## Documentation

The repository contains:

- Technical Documentation PDF
- Project Presentation PPTX
- Source code
- Example input topology
- Generated schedule outputs
- Network visualization
- Automated tests

---

## Author

Nakul Joshi

B.Tech — Computer Science and Engineering

---

## Project Context

Developed as part of the Vaan Megam Networks Wireless Protocol Development Internship assignment.

The project focuses on centralized TDMA scheduling using wireless network graphs, Distance-2 graph coloring, heuristic optimization, schedule validation, spatial reuse, and network visualization.

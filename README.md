TDMA Schedule Planner and Optimizer

A Python-based simulator for centralized TDMA (Time Division Multiple Access) schedule planning in a wireless network using graph theory and NetworkX.

The project models wireless radios as graph nodes and communication links as graph edges. A Distance-2 conflict graph is then constructed to identify nodes that cannot transmit in the same TDMA slot.

Project Objective

The objective is to generate a conflict-free TDMA schedule for a wireless network while allowing spatial reuse of time slots.

The optimizer:

Accepts static coordinates of wireless nodes as JSON input.
Uses a 500-meter communication range to construct the wireless network.
Builds a Distance-2 conflict graph.
Prevents nodes that are 1-hop or 2-hop apart from sharing a slot.
Uses graph-coloring heuristics for TDMA slot assignment.
Evaluates multiple coloring strategies.
Validates the generated schedule.
Produces a Slot × Node Boolean matrix.
Produces a Node → Slot mapping.
Exports the generated schedule to JSON and CSV.
Generates a visualization of the wireless topology and slot assignments.
Technology Stack
Python 3
NetworkX
Pytest
Matplotlib
Graph Theory
TDMA Scheduling
Distance-2 Graph Coloring
System Architecture
Node Coordinates
       │
       ▼
Wireless Network Graph
       │
       │ 500 m communication range
       ▼
Distance-2 Conflict Graph
       │
       ▼
Graph Coloring Heuristics
       │
       ├── Largest First
       ├── Smallest Last
       ├── DSATUR
       └── Randomized Greedy
       │
       ▼
TDMA Slot Assignment
       │
       ├── Node → Slot Mapping
       ├── Slot × Node Matrix
       ├── JSON Output
       └── CSV Output
       │
       ▼
Schedule Validation
Project Structure
tdma-schedule-optimizer/
│
├── docs/
│   ├── VMN_TDMA_Technical_Documentation.pdf
│   └── VMN_TDMA_Schedule_Optimizer_Presentation.pptx
│
├── examples/
│   └── nodes.json
│
├── outputs/
│   ├── schedule.json
│   ├── schedule.csv
│   └── network_topology.png
│
├── src/
│   ├── graph.py
│   ├── main.py
│   ├── scheduler.py
│   └── visualize.py
│
├── tests/
│   └── test_scheduler.py
│
├── .gitignore
├── README.md
└── requirements.txt
How It Works
1. Wireless Network Graph

Each radio is represented as a node.

An edge is created between two nodes when their Euclidean distance is within the configured 500-meter communication range.

Distance(A, B) ≤ 500 m
        │
        ▼
Communication link exists
2. Distance-2 Conflict Graph

The optimizer creates a second graph representing TDMA interference constraints.

Two nodes are considered conflicting when their shortest-path distance in the wireless network is:

1 hop, or
2 hops

Therefore, directly connected nodes and nodes sharing a common neighbor cannot receive the same TDMA slot.

Nodes separated by more than two hops may reuse a slot.

3. Graph Coloring

TDMA slots are represented as graph colors.

Each node receives a color corresponding to its assigned slot.

The optimizer evaluates several coloring strategies:

Largest First
Smallest Last
DSATUR / Saturation Largest First
100 randomized greedy orderings

The coloring using the fewest slots among the evaluated candidates is selected.

The resulting slot count is a heuristic result for the given topology and is not claimed to be the mathematical minimum.

4. Schedule Validation

After coloring, every conflict edge is checked.

A schedule is considered valid when no pair of conflicting nodes has the same slot.

Input Format

The optimizer accepts a JSON file containing node names and their [x, y] coordinates.

Example:

{
    "Node_01": [0.0, 0.0],
    "Node_02": [300.0, 0.0],
    "Node_03": [900.0, 0.0],
    "Node_04": [900.0, 300.0]
}

The supplied example contains 16 wireless nodes.

Running the Optimizer

From the project root:

python src/main.py --input examples/nodes.json

The program generates:

outputs/schedule.json
outputs/schedule.csv

The CLI also displays:

Number of nodes
Number of wireless links
Number of conflict links
Selected coloring strategy
Node-to-slot assignment
Slot × Node matrix
Schedule validation result
Total number of slots
Running the Visualization

After generating the schedule:

python src/visualize.py

This generates:

outputs/network_topology.png

The visualization displays:

Node locations
Wireless links
TDMA slot assignments
Network statistics
Running Tests

Install dependencies:

pip install -r requirements.txt

Run the test suite:

python -m pytest

The test suite covers:

Wireless network graph construction
Distance-2 conflict graph construction
Schedule validity
Schedule matrix generation
Node slot assignment
Non-negative slot values
Node-count validation
Coordinate validation
Non-numeric coordinate validation

Current test result:

9 passed
Optimization Strategy

The optimizer uses multiple graph-coloring approaches rather than relying on a single greedy ordering.

The evaluated strategies are:

Largest First
Smallest Last
DSATUR / Saturation Largest First
100 randomized greedy orderings

The resulting candidate schedules are compared by the number of TDMA slots used, and the candidate with the smallest slot count is selected.

Because graph coloring is computationally difficult in the general case, this implementation uses heuristic optimization rather than claiming an exact globally optimal solution.

Current Result

For the supplied 16-node topology, the implemented heuristic optimizer generates a conflict-free schedule using 7 TDMA slots.

The generated schedule is automatically validated before the output is written.

The current result is a heuristic solution and does not claim that 7 is the theoretical minimum number of slots.

Generated Outputs
Schedule JSON

Contains:

Node coordinates
Network statistics
Node-to-slot assignment
Schedule matrix
Validation result
Total slots
Schedule CSV

Provides the Slot × Node Boolean representation in tabular form.

Network Visualization

Provides a visual representation of:

Wireless links
Node positions
TDMA slot assignments
Network statistics
Validation

The generated schedule is checked against the complete Distance-2 conflict graph.

For every conflict edge:

slot(node_A) != slot(node_B)

must hold.

The current test suite contains 9 automated tests covering graph creation, conflict construction, scheduling, matrix generation, slot validity, and input validation.

Complexity

The wireless graph construction examines pairs of nodes and therefore has quadratic pairwise behavior with respect to the number of nodes.

The Distance-2 conflict graph is constructed using shortest-path distances between node pairs.

The coloring stage uses heuristic graph-coloring algorithms rather than an exact minimum-color solver because the minimum graph-coloring problem is computationally difficult for general graphs.

Part 1 Status

Completed

The centralized Python TDMA Schedule Planner and Optimizer implements the core Part 1 functionality of the assignment.

Part 2 — EMANE Integration

Part 2 is an advanced extension involving EMANE-based wireless simulation.

The planned integration is:

Python TDMA Optimizer
        │
        ▼
Generated TDMA Schedule
        │
        ▼
Schedule Conversion / Bridge
        │
        ▼
EMANE TDMA Radio Model
        │
        ▼
Network Simulation

The EMANE integration is documented as an implementation approach and is separate from the completed centralized Part 1 optimizer.

Engineering Considerations

The current implementation intentionally models interference using a Distance-2 graph abstraction.

This means that nodes within one or two wireless hops are treated as conflicting regardless of detailed physical-layer characteristics.

A future physical-layer implementation could incorporate additional parameters such as:

Signal strength
Interference power
Propagation characteristics
SINR
Radio-specific transmission behavior
Limitations
The optimizer uses heuristic graph coloring.
The selected number of slots is not guaranteed to be globally optimal.
The current model represents interference using Distance-2 graph constraints rather than a detailed physical-layer SINR model.
The current implementation is centralized.
EMANE integration is not required for the core Part 1 implementation.
Reproducibility

The project dependencies are listed in:

requirements.txt

Create a virtual environment:

python -m venv .venv

Activate the environment:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Run tests:

python -m pytest

Run the optimizer:

python src/main.py --input examples/nodes.json

Generate the visualization:

python src/visualize.py
Documentation

The repository includes:

Technical Documentation PDF
Project Presentation PPTX

Both documents provide additional details about the architecture, implementation, results, engineering decisions, limitations, and EMANE integration approach.

Author

Nakul Joshi

B.Tech — Computer Science and Engineering

Project Context

Developed as part of the Vaan Megam Networks Wireless Protocol Development Internship assignment.

The project focuses on centralized TDMA schedule planning using graph modeling, Distance-2 graph coloring, heuristic optimization, schedule validation, and network visualization.

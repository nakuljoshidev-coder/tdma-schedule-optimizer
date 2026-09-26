# TDMA Schedule Planner and Optimizer

A Python-based simulator for scheduling wireless nodes in a TDMA
(Time Division Multiple Access) network using graph algorithms.

## Project Objective

The objective is to create a centralized schedule optimizer that:

- Takes coordinates of 16 wireless nodes as input.
- Creates a wireless network graph based on a 500-meter communication range.
- Identifies 1-hop and 2-hop interference.
- Uses Distance-2 Graph Coloring to assign transmission slots.
- Enables spatial reuse of time slots where possible.
- Generates a conflict-free TDMA schedule.
- Produces a Slot × Node schedule matrix.

## Technology

- Python
- NetworkX
- Graph Theory
- TDMA Scheduling
- Distance-2 Graph Coloring

## Project Structure

```text
tdma-schedule-optimizer/
├── src/
├── examples/
├── tests/
├── docs/
├── README.md
├── requirements.txt
└── .gitignore

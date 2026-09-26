import argparse
import json
import csv
from pathlib import Path

from graph import build_network_graph
from scheduler import (
    build_conflict_graph,
    color_conflict_graph,
    validate_schedule,
    create_schedule_matrix,
)


def load_nodes(input_file):
    """Load and validate node coordinates from a JSON file."""
    with open(input_file, "r", encoding="utf-8") as file:
        nodes = json.load(file)

    if not isinstance(nodes, dict):
        raise ValueError(
            "Input JSON must contain an object of node coordinates."
        )

    if len(nodes) != 16:
        raise ValueError(
            f"Expected exactly 16 nodes, but received {len(nodes)}."
        )

    for node_name, coordinates in nodes.items():
        if not isinstance(coordinates, list) or len(coordinates) != 2:
            raise ValueError(
                f"{node_name} must have coordinates in the form [x, y]."
            )

        if not all(
            isinstance(value, (int, float))
            for value in coordinates
        ):
            raise ValueError(
                f"{node_name} coordinates must contain numeric values."
            )

    return nodes


def save_schedule_json(output_path, slot_assignment, conflicts):
    """Save the generated TDMA schedule as JSON."""
    total_slots = (
        max(slot_assignment.values()) + 1
        if slot_assignment
        else 0
    )

    output_data = {
        "total_slots": total_slots,
        "validation": "VALID" if not conflicts else "INVALID",
        "slot_assignment": slot_assignment,
    }

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=4)


def save_schedule_csv(output_path, nodes, matrix):
    """Save the Slot x Node schedule matrix as CSV."""
    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        writer.writerow(["Slot"] + nodes)

        for slot_number, row in enumerate(matrix):
            writer.writerow(
                [f"Slot {slot_number}"] + row
            )


def main():
    parser = argparse.ArgumentParser(
        description="TDMA Schedule Planner and Optimizer"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the JSON file containing node coordinates.",
    )

    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory where generated schedules will be saved.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    nodes = load_nodes(input_path)

    print("\n" + "=" * 80)
    print("TDMA SCHEDULE PLANNER AND OPTIMIZER")
    print("=" * 80)

    print(f"\nInput file: {input_path}")
    print(f"Total nodes: {len(nodes)}")

    # ---------------------------------------------------------
    # Step 1: Build wireless network graph
    # ---------------------------------------------------------

    network_graph = build_network_graph(nodes)

    print(
        f"Wireless links: "
        f"{network_graph.number_of_edges()}"
    )

    # ---------------------------------------------------------
    # Step 2: Build Distance-2 conflict graph
    # ---------------------------------------------------------

    conflict_graph = build_conflict_graph(
        network_graph
    )

    print(
        f"Conflict links: "
        f"{conflict_graph.number_of_edges()}"
    )

    # ---------------------------------------------------------
    # Step 3: Assign TDMA slots
    # ---------------------------------------------------------

    slot_assignment = color_conflict_graph(
        conflict_graph
    )

    # ---------------------------------------------------------
    # Step 4: Validate schedule
    # ---------------------------------------------------------

    conflicts = validate_schedule(
        conflict_graph,
        slot_assignment
    )

    # ---------------------------------------------------------
    # Step 5: Create Slot x Node matrix
    # ---------------------------------------------------------

    matrix_nodes, matrix = create_schedule_matrix(
        slot_assignment
    )

    total_slots = (
        max(slot_assignment.values()) + 1
        if slot_assignment
        else 0
    )

    # ---------------------------------------------------------
    # Node -> Slot Assignment
    # ---------------------------------------------------------

    print("\n" + "-" * 80)
    print("NODE → SLOT ASSIGNMENT")
    print("-" * 80)

    for node in sorted(slot_assignment):
        print(
            f"{node:<12} → Slot "
            f"{slot_assignment[node]}"
        )

    # ---------------------------------------------------------
    # Schedule Matrix
    # ---------------------------------------------------------

    print("\n" + "-" * 80)
    print("SCHEDULE MATRIX")
    print("-" * 80)

    # Header
    print(
        f"{'Slot':<10}",
        end=""
    )

    for node in matrix_nodes:
        print(
            f"{node:>10}",
            end=""
        )

    print()

    # Rows
    for slot_number, row in enumerate(matrix):
        print(
            f"{f'Slot {slot_number}':<10}",
            end=""
        )

        for value in row:
            print(
                f"{value:>10}",
                end=""
            )

        print()

    # ---------------------------------------------------------
    # Schedule Validation
    # ---------------------------------------------------------

    print("\n" + "-" * 80)
    print("SCHEDULE VALIDATION")
    print("-" * 80)

    if conflicts:
        print(
            "INVALID: Conflicting nodes share "
            "the same TDMA slot."
        )

        for node_a, node_b, slot in conflicts:
            print(
                f"  {node_a} - {node_b} "
                f"→ Slot {slot}"
            )
    else:
        print(
            "VALID: No conflicting nodes share "
            "the same TDMA slot."
        )

    print(f"\nTotal slots used: {total_slots}")

    # ---------------------------------------------------------
    # Save outputs
    # ---------------------------------------------------------

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    json_output = output_dir / "schedule.json"
    csv_output = output_dir / "schedule.csv"

    save_schedule_json(
        json_output,
        slot_assignment,
        conflicts
    )

    save_schedule_csv(
        csv_output,
        matrix_nodes,
        matrix
    )

    print("\n" + "-" * 80)
    print("OUTPUT FILES")
    print("-" * 80)

    print(f"JSON: {json_output}")
    print(f"CSV : {csv_output}")

    print("\nOptimization completed successfully.")
    print("=" * 80)


if __name__ == "__main__":
    main()
import json
import csv
import os

from graph import build_network_graph

from scheduler import (
    build_conflict_graph,
    color_conflict_graph,
    validate_schedule,
    create_schedule_matrix
)


def load_nodes(filename):
    """Load node coordinates from JSON."""

    with open(filename, "r") as file:
        return json.load(file)


def save_schedule_json(
    filename,
    slot_assignment,
    total_slots,
    validation_status
):
    """Save the TDMA schedule as JSON."""

    data = {
        "total_slots": total_slots,
        "validation": validation_status,
        "slot_assignment": slot_assignment
    }

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def save_schedule_csv(
    filename,
    nodes,
    matrix
):
    """Save the TDMA Slot x Node matrix as CSV."""

    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        # Header
        writer.writerow(
            ["Slot"] + nodes
        )

        # Matrix
        for slot_number, row in enumerate(matrix):

            writer.writerow(
                [slot_number] + row
            )


def main():

    # ==================================================
    # 1. LOAD NODE DATA
    # ==================================================

    nodes = load_nodes(
        "../examples/nodes.json"
    )


    # ==================================================
    # 2. BUILD WIRELESS NETWORK
    # ==================================================

    network_graph = build_network_graph(
        nodes
    )


    # ==================================================
    # 3. BUILD DISTANCE-2 CONFLICT GRAPH
    # ==================================================

    conflict_graph = build_conflict_graph(
        network_graph
    )


    # ==================================================
    # 4. COLOR CONFLICT GRAPH
    # ==================================================

    slot_assignment = color_conflict_graph(
        conflict_graph
    )


    # ==================================================
    # 5. CALCULATE SLOT COUNT
    # ==================================================

    total_slots = (
        max(slot_assignment.values()) + 1
    )


    # ==================================================
    # 6. VALIDATE SCHEDULE
    # ==================================================

    conflicts = validate_schedule(
        conflict_graph,
        slot_assignment
    )

    schedule_valid = len(conflicts) == 0


    # ==================================================
    # 7. CREATE SCHEDULE MATRIX
    # ==================================================

    matrix_nodes, matrix = create_schedule_matrix(
        slot_assignment
    )


    # ==================================================
    # 8. CREATE OUTPUT DIRECTORY
    # ==================================================

    output_directory = "../outputs"

    os.makedirs(
        output_directory,
        exist_ok=True
    )


    # ==================================================
    # 9. SAVE JSON
    # ==================================================

    json_file = os.path.join(
        output_directory,
        "schedule.json"
    )

    save_schedule_json(
        json_file,
        slot_assignment,
        total_slots,
        "VALID" if schedule_valid else "INVALID"
    )


    # ==================================================
    # 10. SAVE CSV
    # ==================================================

    csv_file = os.path.join(
        output_directory,
        "schedule.csv"
    )

    save_schedule_csv(
        csv_file,
        matrix_nodes,
        matrix
    )


    # ==================================================
    # 11. DISPLAY NETWORK
    # ==================================================

    print("\nTDMA NETWORK TOPOLOGY")
    print("=" * 60)

    print(
        f"Total nodes: "
        f"{len(network_graph.nodes)}"
    )

    print(
        f"Total wireless links: "
        f"{len(network_graph.edges)}"
    )


    # ==================================================
    # 12. DISPLAY CONFLICT GRAPH
    # ==================================================

    print("\nDISTANCE-2 CONFLICT GRAPH")
    print("-" * 60)

    print(
        f"Total conflict links: "
        f"{len(conflict_graph.edges)}"
    )


    # ==================================================
    # 13. DISPLAY SLOT ASSIGNMENTS
    # ==================================================

    print("\nTDMA SLOT ASSIGNMENTS")
    print("-" * 60)

    for node, slot in sorted(
        slot_assignment.items()
    ):

        print(
            f"{node}: Slot {slot}"
        )


    print("\n" + "=" * 60)

    print(
        f"Total slots used: "
        f"{total_slots}"
    )

    print("=" * 60)


    # ==================================================
    # 14. VALIDATION
    # ==================================================

    print("\nSCHEDULE VALIDATION")
    print("-" * 60)

    if schedule_valid:

        print(
            "VALID: No conflicting nodes "
            "share the same TDMA slot."
        )

    else:

        print(
            f"INVALID: {len(conflicts)} "
            f"conflict(s) detected."
        )

        for node_a, node_b, slot in conflicts:

            print(
                f"{node_a} and {node_b} "
                f"both use Slot {slot}"
            )


    # ==================================================
    # 15. OUTPUT FILES
    # ==================================================

    print("\nOUTPUT FILES")
    print("-" * 60)

    print(
        f"JSON: {json_file}"
    )

    print(
        f"CSV : {csv_file}"
    )


if __name__ == "__main__":
    main()
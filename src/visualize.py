import json
from pathlib import Path

import matplotlib.pyplot as plt

from graph import build_network_graph


RADIO_RANGE = 500.0


def load_nodes(input_path):
    """Load node coordinates from a JSON file."""

    with open(input_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_schedule(schedule_path):
    """Load the generated TDMA schedule."""

    with open(schedule_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["slot_assignment"]


def visualize_network(nodes, slot_assignment, output_path):
    """
    Generate a visualization of the wireless network.

    Nodes are positioned according to their coordinates.
    Wireless links represent communication relationships
    within the 500-meter radio range.

    Node colors represent their assigned TDMA slots.
    """

    graph = build_network_graph(nodes)

    plt.figure(figsize=(12, 9))

    # ---------------------------------------------------------
    # Draw wireless communication links
    # ---------------------------------------------------------

    for node_a, node_b in graph.edges():

        x1, y1 = nodes[node_a]
        x2, y2 = nodes[node_b]

        plt.plot(
            [x1, x2],
            [y1, y2],
            color="gray",
            linewidth=1,
            alpha=0.5,
            zorder=1
        )

    # ---------------------------------------------------------
    # Group nodes by TDMA slot
    # ---------------------------------------------------------

    slots = sorted(
        set(slot_assignment.values())
    )

    cmap = plt.get_cmap("tab10")

    # ---------------------------------------------------------
    # Plot nodes
    # ---------------------------------------------------------

    for slot in slots:

        slot_nodes = [
            node
            for node in nodes
            if slot_assignment[node] == slot
        ]

        x_coordinates = [
            nodes[node][0]
            for node in slot_nodes
        ]

        y_coordinates = [
            nodes[node][1]
            for node in slot_nodes
        ]

        plt.scatter(
            x_coordinates,
            y_coordinates,
            s=180,
            color=cmap(slot % 10),
            label=f"Slot {slot}",
            edgecolors="black",
            linewidths=1,
            zorder=2
        )

    # ---------------------------------------------------------
    # Add node labels
    # ---------------------------------------------------------

    for node, coordinates in nodes.items():

        x, y = coordinates

        slot = slot_assignment[node]

        plt.annotate(
            f"{node}\nS{slot}",
            (x, y),
            xytext=(7, 7),
            textcoords="offset points",
            fontsize=9,
            zorder=3
        )

    # ---------------------------------------------------------
    # Draw communication radius
    # ---------------------------------------------------------

    # The circles are intentionally not drawn around every node
    # because overlapping 500 m circles can make the diagram
    # difficult to read.

    plt.title(
        "TDMA Wireless Network Topology\n"
        "Node Position, Communication Links and TDMA Slots",
        fontsize=15
    )

    plt.xlabel("X Coordinate (meters)")
    plt.ylabel("Y Coordinate (meters)")

    plt.legend(
        title="TDMA Slots",
        loc="best"
    )

    plt.grid(
        True,
        linestyle="--",
        alpha=0.3
    )

    plt.axis("equal")

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


def main():

    # ---------------------------------------------------------
    # Project paths
    # ---------------------------------------------------------

    project_root = Path(__file__).resolve().parent.parent

    input_path = (
        project_root
        / "examples"
        / "nodes.json"
    )

    schedule_path = (
        project_root
        / "outputs"
        / "schedule.json"
    )

    output_path = (
        project_root
        / "outputs"
        / "network_topology.png"
    )

    # ---------------------------------------------------------
    # Validate required files
    # ---------------------------------------------------------

    if not input_path.exists():

        raise FileNotFoundError(
            f"Node input file not found: {input_path}"
        )

    if not schedule_path.exists():

        raise FileNotFoundError(
            "Schedule file not found.\n"
            "Run the optimizer first:\n\n"
            "python src/main.py "
            "--input examples/nodes.json"
        )

    # ---------------------------------------------------------
    # Load data
    # ---------------------------------------------------------

    nodes = load_nodes(input_path)

    slot_assignment = load_schedule(
        schedule_path
    )

    # ---------------------------------------------------------
    # Generate visualization
    # ---------------------------------------------------------

    visualize_network(
        nodes,
        slot_assignment,
        output_path
    )

    print("\nVisualization generated successfully.")

    print(
        f"Saved to: {output_path}"
    )


if __name__ == "__main__":
    main()
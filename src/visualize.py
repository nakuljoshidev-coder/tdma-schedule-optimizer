import json
from pathlib import Path

import matplotlib.pyplot as plt

from graph import build_network_graph


def load_nodes(input_path):
    """Load node coordinates from JSON."""
    with open(input_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_schedule(schedule_path):
    """Load the generated TDMA schedule."""
    with open(schedule_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def visualize_network(nodes, schedule_data, output_path):
    """
    Generate a presentation-quality visualization of the TDMA network.

    The figure shows:
    - Node positions
    - Wireless links within 500 m
    - TDMA slot assignment
    - Network statistics
    """

    slot_assignment = schedule_data["slot_assignment"]
    total_slots = schedule_data["total_slots"]
    validation = schedule_data["validation"]

    graph = build_network_graph(nodes)

    # ---------------------------------------------------------
    # Create figure
    # ---------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(15, 10)
    )

    # ---------------------------------------------------------
    # Draw wireless communication links
    # ---------------------------------------------------------

    for node_a, node_b in graph.edges():

        x1, y1 = nodes[node_a]
        x2, y2 = nodes[node_b]

        ax.plot(
            [x1, x2],
            [y1, y2],
            linewidth=1.2,
            alpha=0.35,
            zorder=1
        )

    # ---------------------------------------------------------
    # Determine slots
    # ---------------------------------------------------------

    slots = sorted(
        set(slot_assignment.values())
    )

    cmap = plt.get_cmap("tab10")

    # ---------------------------------------------------------
    # Draw nodes grouped by TDMA slot
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

        ax.scatter(
            x_coordinates,
            y_coordinates,
            s=260,
            color=cmap(slot % 10),
            edgecolors="black",
            linewidths=1.5,
            label=f"Slot {slot}",
            zorder=3
        )

    # ---------------------------------------------------------
    # Node labels
    # ---------------------------------------------------------

    for node, coordinates in nodes.items():

        x, y = coordinates
        slot = slot_assignment[node]

        ax.annotate(
            f"{node}\nSlot {slot}",
            (x, y),
            xytext=(8, 8),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
            zorder=4
        )

    # ---------------------------------------------------------
    # Title
    # ---------------------------------------------------------

    ax.set_title(
        "TDMA Schedule Planner — Wireless Network Topology",
        fontsize=20,
        fontweight="bold",
        pad=20
    )

    ax.text(
        0.5,
        1.015,
        "500 m Communication Range • Distance-2 Conflict Scheduling",
        transform=ax.transAxes,
        ha="center",
        fontsize=11
    )

    # ---------------------------------------------------------
    # Axis labels
    # ---------------------------------------------------------

    ax.set_xlabel(
        "X Coordinate (meters)",
        fontsize=12
    )

    ax.set_ylabel(
        "Y Coordinate (meters)",
        fontsize=12
    )

    # ---------------------------------------------------------
    # Network statistics box
    # ---------------------------------------------------------

    statistics = (
        f"NETWORK STATISTICS\n"
        f"Nodes: {len(nodes)}\n"
        f"Wireless Links: {graph.number_of_edges()}\n"
        f"Communication Range: 500 m\n"
        f"TDMA Slots: {total_slots}\n"
        f"Schedule: {validation}"
    )

    ax.text(
        0.02,
        0.97,
        statistics,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round,pad=0.6",
            alpha=0.9
        ),
        zorder=5
    )

    # ---------------------------------------------------------
    # Legend
    # ---------------------------------------------------------

    legend = ax.legend(
        title="TDMA Slot",
        loc="upper right",
        fontsize=10,
        title_fontsize=11
    )

    legend.get_frame().set_alpha(0.9)

    # ---------------------------------------------------------
    # Grid
    # ---------------------------------------------------------

    ax.grid(
        True,
        linestyle="--",
        alpha=0.25
    )

    # Keep X/Y scale equal so physical distances are represented
    # correctly.
    ax.set_aspect("equal", adjustable="box")

    # ---------------------------------------------------------
    # Layout
    # ---------------------------------------------------------

    plt.tight_layout()

    # ---------------------------------------------------------
    # Save high-resolution image
    # ---------------------------------------------------------

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


def main():

    # ---------------------------------------------------------
    # Locate project files
    # ---------------------------------------------------------

    project_root = (
        Path(__file__).resolve().parent.parent
    )

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
    # Validate files
    # ---------------------------------------------------------

    if not input_path.exists():

        raise FileNotFoundError(
            f"Node input file not found:\n{input_path}"
        )

    if not schedule_path.exists():

        raise FileNotFoundError(
            "Schedule file not found.\n\n"
            "Run the optimizer first:\n"
            "python src/main.py "
            "--input examples/nodes.json"
        )

    # ---------------------------------------------------------
    # Load data
    # ---------------------------------------------------------

    nodes = load_nodes(
        input_path
    )

    schedule_data = load_schedule(
        schedule_path
    )

    # ---------------------------------------------------------
    # Generate visualization
    # ---------------------------------------------------------

    visualize_network(
        nodes,
        schedule_data,
        output_path
    )

    print()
    print("=" * 60)
    print("NETWORK VISUALIZATION")
    print("=" * 60)
    print()
    print("Visualization generated successfully.")
    print(f"Saved to: {output_path}")
    print()


if __name__ == "__main__":
    main()
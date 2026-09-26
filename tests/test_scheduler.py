import sys
import os

import networkx as nx

# Add the src directory to Python's import path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src"
        )
    )
)

from graph import build_network_graph
from scheduler import (
    build_conflict_graph,
    color_conflict_graph,
    validate_schedule,
    create_schedule_matrix,
)


def test_network_graph_is_created():
    """
    Test that the wireless network graph
    is created correctly from node coordinates.
    """

    nodes = {
        "A": [0, 0],
        "B": [300, 0],
        "C": [1000, 0],
    }

    graph = build_network_graph(nodes)

    assert isinstance(graph, nx.Graph)

    assert len(graph.nodes) == 3

    # A and B are 300 m apart,
    # so they should have a wireless link.
    assert graph.has_edge("A", "B")

    # A and C are 1000 m apart,
    # so they should NOT have a wireless link.
    assert not graph.has_edge("A", "C")


def test_conflict_graph_contains_wireless_links():
    """
    Test that directly connected wireless nodes
    appear in the conflict graph.
    """

    network = nx.Graph()

    network.add_edge("A", "B")
    network.add_edge("B", "C")

    conflict_graph = build_conflict_graph(network)

    assert conflict_graph.has_edge("A", "B")
    assert conflict_graph.has_edge("B", "C")


def test_schedule_has_no_conflicts():
    """
    Test that the generated TDMA schedule
    does not assign the same slot to conflicting nodes.
    """

    network = nx.Graph()

    network.add_edges_from([
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
    ])

    conflict_graph = build_conflict_graph(network)

    slot_assignment = color_conflict_graph(
        conflict_graph
    )

    conflicts = validate_schedule(
        conflict_graph,
        slot_assignment
    )

    assert conflicts == []


def test_schedule_matrix():
    """
    Test that the Slot x Node matrix
    is generated correctly.
    """

    slot_assignment = {
        "A": 0,
        "B": 1,
        "C": 0,
    }

    nodes, matrix = create_schedule_matrix(
        slot_assignment
    )

    assert nodes == ["A", "B", "C"]

    assert matrix[0] == [1, 0, 1]
    assert matrix[1] == [0, 1, 0]


def test_every_node_has_a_slot():
    """
    Test that every node receives a TDMA slot.
    """

    network = nx.Graph()

    network.add_edges_from([
        ("A", "B"),
        ("B", "C"),
    ])

    conflict_graph = build_conflict_graph(
        network
    )

    slot_assignment = color_conflict_graph(
        conflict_graph
    )

    assert set(slot_assignment.keys()) == {
        "A",
        "B",
        "C",
    }


def test_slots_are_non_negative():
    """
    Test that no node receives an invalid
    negative TDMA slot.
    """

    network = nx.Graph()

    network.add_edges_from([
        ("A", "B"),
        ("B", "C"),
    ])

    conflict_graph = build_conflict_graph(
        network
    )

    slot_assignment = color_conflict_graph(
        conflict_graph
    )

    for slot in slot_assignment.values():
        assert slot >= 0
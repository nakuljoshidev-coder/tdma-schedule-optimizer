import sys
import os
import json

import networkx as nx
import pytest

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
from main import load_nodes


def test_network_graph_is_created():
    nodes = {
        "A": [0, 0],
        "B": [300, 0],
        "C": [1000, 0],
    }

    graph = build_network_graph(nodes)

    assert isinstance(graph, nx.Graph)
    assert len(graph.nodes) == 3
    assert graph.has_edge("A", "B")
    assert not graph.has_edge("A", "C")


def test_conflict_graph_contains_wireless_links():
    network = nx.Graph()

    network.add_edge("A", "B")
    network.add_edge("B", "C")

    conflict_graph = build_conflict_graph(network)

    assert conflict_graph.has_edge("A", "B")
    assert conflict_graph.has_edge("B", "C")


def test_schedule_has_no_conflicts():
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
    network = nx.Graph()

    network.add_edges_from([
        ("A", "B"),
        ("B", "C"),
    ])

    conflict_graph = build_conflict_graph(network)

    slot_assignment = color_conflict_graph(
        conflict_graph
    )

    assert set(slot_assignment.keys()) == {
        "A",
        "B",
        "C",
    }


def test_slots_are_non_negative():
    network = nx.Graph()

    network.add_edges_from([
        ("A", "B"),
        ("B", "C"),
    ])

    conflict_graph = build_conflict_graph(network)

    slot_assignment = color_conflict_graph(
        conflict_graph
    )

    for slot in slot_assignment.values():
        assert slot >= 0


def test_input_requires_16_nodes(tmp_path):
    nodes = {
        "Node_01": [0, 0],
        "Node_02": [300, 0],
    }

    input_file = tmp_path / "invalid_nodes.json"

    with open(input_file, "w", encoding="utf-8") as file:
        json.dump(nodes, file)

    with pytest.raises(ValueError, match="exactly 16 nodes"):
        load_nodes(input_file)


def test_input_rejects_invalid_coordinates(tmp_path):
    nodes = {
        f"Node_{i:02d}": [0, 0]
        for i in range(1, 17)
    }

    nodes["Node_01"] = [0]

    input_file = tmp_path / "invalid_coordinates.json"

    with open(input_file, "w", encoding="utf-8") as file:
        json.dump(nodes, file)

    with pytest.raises(
        ValueError,
        match="must have coordinates"
    ):
        load_nodes(input_file)


def test_input_rejects_non_numeric_coordinates(tmp_path):
    nodes = {
        f"Node_{i:02d}": [0, 0]
        for i in range(1, 17)
    }

    nodes["Node_01"] = ["x", 0]

    input_file = tmp_path / "invalid_values.json"

    with open(input_file, "w", encoding="utf-8") as file:
        json.dump(nodes, file)

    with pytest.raises(
        ValueError,
        match="must contain numeric values"
    ):
        load_nodes(input_file)
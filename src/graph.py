import math
import networkx as nx


RADIO_RANGE = 500.0


def calculate_distance(node1, node2):
    """
    Calculate the Euclidean distance between two nodes.

    node1 and node2 are coordinates in the form:
    [x, y]
    """

    x1, y1 = node1
    x2, y2 = node2

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return distance


def build_network_graph(nodes):
    """
    Build a wireless network graph.

    Each node represents a radio.
    An edge is created when two radios are within 500 meters.
    """

    graph = nx.Graph()

    # Add all radios as graph nodes
    for node_name in nodes:
        graph.add_node(node_name)

    node_names = list(nodes.keys())

    # Check every pair of radios
    for i in range(len(node_names)):
        for j in range(i + 1, len(node_names)):

            node_a = node_names[i]
            node_b = node_names[j]

            distance = calculate_distance(
                nodes[node_a],
                nodes[node_b]
            )

            # Radios within 500 meters can communicate
            if distance <= RADIO_RANGE:
                graph.add_edge(
                    node_a,
                    node_b,
                    distance=distance
                )

    return graph
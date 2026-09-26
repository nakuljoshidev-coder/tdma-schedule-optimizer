import json

from graph import build_network_graph


def load_nodes(filename):
    """Load node coordinates from a JSON file."""

    with open(filename, "r") as file:
        nodes = json.load(file)

    return nodes


def main():
    nodes = load_nodes("../examples/nodes.json")

    graph = build_network_graph(nodes)

    print("\nTDMA NETWORK TOPOLOGY")
    print("=" * 40)

    print(f"Total nodes: {len(graph.nodes)}")
    print(f"Total links: {len(graph.edges)}")

    print("\nWIRELESS CONNECTIONS")
    print("-" * 40)

    for node_a, node_b, data in graph.edges(data=True):

        distance = data["distance"]

        print(
            f"{node_a} <----> {node_b} "
            f"({distance:.2f} m)"
        )


if __name__ == "__main__":
    main()
import random

import networkx as nx


def build_conflict_graph(network_graph):
    """
    Build the Distance-2 conflict graph.

    Two nodes are considered conflicting when their shortest-path
    distance in the wireless network is 1 or 2 hops.

    Therefore:
        1-hop neighbors cannot share a slot.
        2-hop neighbors cannot share a slot.
        Nodes more than 2 hops apart may reuse a slot.
    """

    conflict_graph = nx.Graph()

    # Every wireless node must also exist in the conflict graph.
    conflict_graph.add_nodes_from(network_graph.nodes)

    nodes = list(network_graph.nodes)

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):

            node_a = nodes[i]
            node_b = nodes[j]

            try:
                hop_distance = nx.shortest_path_length(
                    network_graph,
                    node_a,
                    node_b
                )

            except nx.NetworkXNoPath:
                # Disconnected nodes cannot interfere through
                # a 1-hop or 2-hop path.
                continue

            if hop_distance <= 2:
                conflict_graph.add_edge(
                    node_a,
                    node_b,
                    hop_distance=hop_distance
                )

    return conflict_graph


def count_slots(slot_assignment):
    """
    Return the number of TDMA slots used.

    Slot numbers start at zero, so the highest slot number
    plus one gives the total number of slots.
    """

    if not slot_assignment:
        return 0

    return max(slot_assignment.values()) + 1


def greedy_color_random_order(conflict_graph, seed):
    """
    Perform greedy graph coloring using a deterministic
    shuffled node order.

    A seed is used so that the result can be reproduced.
    """

    nodes = list(conflict_graph.nodes)

    random_generator = random.Random(seed)
    random_generator.shuffle(nodes)

    assignment = {}

    for node in nodes:

        unavailable_slots = {
            assignment[neighbor]
            for neighbor in conflict_graph.neighbors(node)
            if neighbor in assignment
        }

        slot = 0

        while slot in unavailable_slots:
            slot += 1

        assignment[node] = slot

    return assignment


def generate_coloring_candidates(conflict_graph):
    """
    Generate multiple graph-coloring candidates.

    The optimizer evaluates several ordering strategies because
    greedy graph coloring is heuristic and different node
    orderings can produce different numbers of slots.
    """

    candidates = []

    # ---------------------------------------------------------
    # Strategy 1: Largest First
    # ---------------------------------------------------------

    assignment = nx.coloring.greedy_color(
        conflict_graph,
        strategy="largest_first"
    )

    candidates.append(
        ("largest_first", assignment)
    )

    # ---------------------------------------------------------
    # Strategy 2: Smallest Last
    # ---------------------------------------------------------

    assignment = nx.coloring.greedy_color(
        conflict_graph,
        strategy="smallest_last"
    )

    candidates.append(
        ("smallest_last", assignment)
    )

    # ---------------------------------------------------------
    # Strategy 3: DSATUR
    # ---------------------------------------------------------

    assignment = nx.coloring.greedy_color(
        conflict_graph,
        strategy="saturation_largest_first"
    )

    candidates.append(
        ("DSATUR", assignment)
    )

    # ---------------------------------------------------------
    # Strategy 4: Deterministic randomized greedy
    # ---------------------------------------------------------

    for trial in range(100):

        seed = trial + 1

        assignment = greedy_color_random_order(
            conflict_graph,
            seed
        )

        candidates.append(
            (
                f"random_greedy_{trial + 1}",
                assignment
            )
        )

    return candidates


def color_conflict_graph(conflict_graph):
    """
    Find a low-slot TDMA coloring using multiple heuristics.

    The exact minimum graph coloring problem is computationally
    difficult for general graphs. Therefore, this implementation
    evaluates multiple greedy coloring strategies and selects
    the valid candidate using the fewest slots.

    Returns:
        dict:
            Node -> assigned TDMA slot
    """

    candidates = generate_coloring_candidates(
        conflict_graph
    )

    best_strategy = None
    best_assignment = None
    best_slot_count = float("inf")

    for strategy, assignment in candidates:

        slot_count = count_slots(
            assignment
        )

        if slot_count < best_slot_count:

            best_slot_count = slot_count
            best_assignment = assignment
            best_strategy = strategy

    print("\nCOLORING OPTIMIZATION")
    print("-" * 60)

    print(
        f"Strategies tested: {len(candidates)}"
    )

    print(
        f"Selected strategy: {best_strategy}"
    )

    print(
        f"Slots used: {best_slot_count}"
    )

    return best_assignment


def validate_schedule(conflict_graph, slot_assignment):
    """
    Verify that no conflicting nodes share a TDMA slot.

    Returns:
        list:
            Conflicting node pairs and their shared slot.
    """

    conflicts = []

    for node_a, node_b in conflict_graph.edges():

        if slot_assignment[node_a] == slot_assignment[node_b]:

            conflicts.append(
                (
                    node_a,
                    node_b,
                    slot_assignment[node_a]
                )
            )

    return conflicts


def create_schedule_matrix(slot_assignment):
    """
    Create a Slot x Node boolean matrix.

    Matrix meaning:

        1 -> node transmits in this slot
        0 -> node does not transmit in this slot

    Returns:
        nodes:
            Sorted list of node names.

        matrix:
            List of rows representing TDMA slots.
    """

    nodes = sorted(
        slot_assignment.keys()
    )

    total_slots = count_slots(
        slot_assignment
    )

    matrix = []

    for slot in range(total_slots):

        row = []

        for node in nodes:

            if slot_assignment[node] == slot:
                row.append(1)
            else:
                row.append(0)

        matrix.append(row)

    return nodes, matrix
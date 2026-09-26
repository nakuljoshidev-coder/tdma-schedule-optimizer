import random
import networkx as nx


def build_conflict_graph(network_graph):
    """
    Build a Distance-2 conflict graph.

    Nodes conflict when their shortest-path distance
    in the wireless network is 1 or 2 hops.
    """

    conflict_graph = nx.Graph()

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
                continue

            if hop_distance <= 2:
                conflict_graph.add_edge(
                    node_a,
                    node_b,
                    hop_distance=hop_distance
                )

    return conflict_graph


def count_slots(slot_assignment):
    """Return the number of TDMA slots used."""

    if not slot_assignment:
        return 0

    return max(slot_assignment.values()) + 1


def color_conflict_graph(conflict_graph):
    """
    Optimize TDMA slot assignment.

    Multiple coloring heuristics are tested and the coloring
    using the fewest slots is selected.
    """

    candidates = []

    # --------------------------------------------------
    # 1. Largest-first
    # --------------------------------------------------

    assignment = nx.coloring.greedy_color(
        conflict_graph,
        strategy="largest_first"
    )

    candidates.append(
        ("largest_first", assignment)
    )

    # --------------------------------------------------
    # 2. Smallest-last
    # --------------------------------------------------

    assignment = nx.coloring.greedy_color(
        conflict_graph,
        strategy="smallest_last"
    )

    candidates.append(
        ("smallest_last", assignment)
    )

    # --------------------------------------------------
    # 3. DSATUR
    # --------------------------------------------------

    assignment = nx.coloring.greedy_color(
        conflict_graph,
        strategy="saturation_largest_first"
    )

    candidates.append(
        ("DSATUR", assignment)
    )

    # --------------------------------------------------
    # 4. Randomized greedy coloring
    # --------------------------------------------------

    nodes = list(conflict_graph.nodes)

    for trial in range(100):

        random.shuffle(nodes)

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

        candidates.append(
            (
                f"random_greedy_{trial + 1}",
                assignment
            )
        )

    # --------------------------------------------------
    # Select best valid coloring
    # --------------------------------------------------

    best_strategy = None
    best_assignment = None
    best_slot_count = float("inf")

    for strategy, assignment in candidates:

        slot_count = count_slots(assignment)

        if slot_count < best_slot_count:

            best_slot_count = slot_count
            best_assignment = assignment
            best_strategy = strategy

    # --------------------------------------------------
    # Print optimization result
    # --------------------------------------------------

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

    1 = node transmits in that slot
    0 = node does not transmit
    """

    nodes = sorted(slot_assignment.keys())

    total_slots = count_slots(slot_assignment)

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
"""
Search 2 algorithm with Initial Degree Ordering (Pablo San Segundo approach).
Initial Sorting of Vertices in the Maximum Clique Problem Reviewed — Pablo San Segundo et al., 2014. csplib.org
https://link.springer.com/chapter/10.1007/978-3-642-11440-3_18
"""

import sys
from parser import parse_dimacs_graph

def is_clique(graph, nodes):
    """Check if the given nodes form a clique."""
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if nodes[j] not in graph[nodes[i]]:
                return False
    return True

def search_max_clique(graph):
    """
    Branch and Bound (your search2) + initial vertex ordering by degree (descending).
    The rest of the logic is unchanged, so you can isolate the effect of ordering.
    """
    # --- NEW: initial sorting (San Segundo et al., 2014) ---
    deg = {v: len(graph[v]) for v in graph}
    # Sort vertices by degree descending; stable tie-breaker on vertex id
    vertices = sorted(graph.keys(), key=lambda v: (deg[v], v), reverse=True)

    max_clique = []

    def heuristic(current, remaining):
        # Simple bound: current size + remaining candidates
        return len(current) + len(remaining)

    def backtrack(current, remaining, depth=0):
        nonlocal max_clique

        # Update best
        if len(current) > len(max_clique):
            max_clique = current[:]

        # Global prune for this node
        if heuristic(current, remaining) <= len(max_clique):
            return

        # Try adding each remaining vertex (preserves the initial degree order)
        for i in range(len(remaining)):
            vertex = remaining[i]

            # Must connect to all in current
            if all(neighbor in graph[vertex] for neighbor in current):
                # Build next candidate list (still a list, preserves order)
                new_remaining = []
                for v in remaining[i+1:]:
                    is_connected = True
                    for c in current:
                        if v not in graph[c]:
                            is_connected = False
                            break
                    if is_connected and v in graph[vertex]:
                        new_remaining.append(v)

                # Optional local prune before recursing (kept identical to your search2)
                if heuristic(current + [vertex], new_remaining) <= len(max_clique):
                    continue  # prune this branch and the rest at this depth (same behaviour as your code)

                backtrack(current + [vertex], new_remaining, depth + 1)

    backtrack([], vertices)
    return max_clique

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py <graph_file>")
        sys.exit(1)

    filename = sys.argv[1]
    num_vertices, edges = parse_dimacs_graph(filename)

    # Adjacency as sets (same as before)
    graph = {i: set() for i in range(1, num_vertices + 1)}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    result = search_max_clique(graph)
    print(f"Maximum clique size: {len(result)}")
    print(f"Maximum clique: {sorted(result)}")

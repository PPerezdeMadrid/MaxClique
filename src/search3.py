"""
Search 2 algorithm with Initial Degree Ordering (Pablo San Segundo approach).
Initial Sorting of Vertices in the Maximum Clique Problem Reviewed — Pablo San Segundo et al., 2014. csplib.org
https://link.springer.com/chapter/10.1007/978-3-642-11440-3_18
"""

import sys
from parser import parse_dimacs_graph

def is_clique(graph, nodes):
    """Return True if all nodes are pairwise connected."""
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if nodes[j] not in graph[nodes[i]]:
                return False
    return True

def search_max_clique(graph):
    """BnB with Initial Degree Ordering."""
    # Order vertices by descending degree; tie-break by id
    deg = {v: len(graph[v]) for v in graph} # degree map
    vertices = sorted(graph.keys(), key=lambda v: (deg[v], v), reverse=True) # ordered vertices
    

    max_clique = []

    def heuristic(current, remaining):
        # Upper bound: what we have + what we could still add
        return len(current) + len(remaining)

    def backtrack(current, remaining, depth=0):
        nonlocal max_clique

        if len(current) > len(max_clique):
            max_clique = current[:]

        # Stop if even the best-case here can’t beat the best so far
        if heuristic(current, remaining) <= len(max_clique):
            return

        # Explore in the precomputed order
        for i in range(len(remaining)):
            vertex = remaining[i]

            # v must connect to everyone in current
            if all(neighbour in graph[vertex] for neighbour in current):
                # Rebuild next candidates (intentionally simple/inefficient)
                next_remaining = []
                for other in remaining[i + 1:]:
                    is_connected = True
                    for v_in_clique in current:
                        if other not in graph[v_in_clique]:
                            is_connected = False
                            break
                    if is_connected and other in graph[vertex]:
                        next_remaining.append(other)

                # Local prune as search2
                if heuristic(current + [vertex], next_remaining) <= len(max_clique):
                    continue

                backtrack(current + [vertex], next_remaining, depth + 1)

    backtrack([], vertices)
    return max_clique

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py <graph_file>")
        sys.exit(1)

    filename = sys.argv[1]
    n, edges = parse_dimacs_graph(filename)

    # Build adjacency sets
    graph = {i: set() for i in range(1, n + 1)}
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)

    clique = search_max_clique(graph)
    print(f"Maximum clique size: {len(clique)}")
    print(f"Maximum clique: {sorted(clique)}")

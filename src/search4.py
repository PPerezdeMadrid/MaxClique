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
    deg = {v: len(graph[v]) for v in graph}
    vertices = sorted(graph.keys(), key=lambda v: (deg[v], v), reverse=True)

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
            v = remaining[i]

            # v must connect to everyone in current
            if all(u in graph[v] for u in current):
                # Next candidates: keep order, keep only those linked to current and v
                next_remaining = []
                for w in remaining[i + 1:]:
                    ok = True
                    for c in current:
                        if w not in graph[c]:
                            ok = False
                            break
                    if ok and w in graph[v]:
                        next_remaining.append(w)

                # Local prune as search2
                if heuristic(current + [v], next_remaining) <= len(max_clique):
                    continue

                backtrack(current + [v], next_remaining, depth + 1)

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

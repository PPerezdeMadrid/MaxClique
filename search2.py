"""
Basic implementation of Branch and Bound.
Based on: A Simple and Faster Branch-and‑Bound Algorithm for Finding a Maximum Clique — Etsuji Tomita et al., 2010.  ==> ¡https://link.springer.com/chapter/10.1007/978-3-642-11440-3_18
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
    """Pruning added to the original algorithm."""
    vertices = list(graph.keys())
    max_clique = []

    def heuristic(current, remaining):
        # Best case from here: what we have + candidates left
        return len(current) + len(remaining)

    def backtrack(current, remaining, depth=0):
        nonlocal max_clique

        if len(current) > len(max_clique):
            max_clique = current[:]

        # Stop if this branch can’t beat the best so far
        if heuristic(current, remaining) <= len(max_clique):
            return

        # Try each next vertex
        for i in range(len(remaining)):
            v = remaining[i]

            # v must connect to everyone in current
            if all(u in graph[v] for u in current):
                # Rebuild next candidates (intentionally simple/inefficient)
                next_remaining = []
                for w in remaining[i + 1:]:
                    ok = True
                    for c in current:
                        if w not in graph[c]:
                            ok = False
                            break
                    if ok and w in graph[v]:
                        next_remaining.append(w)

                # Local prune before diving deeper
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
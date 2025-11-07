"""
Search 2 algorithm with a Greedy Colouring Bound (Etsuji Tomita approach).
A Simple and Faster Branch-and‑Bound Algorithm for Finding a Maximum Clique — Etsuji Tomita et al., 2010. 
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
    B&B with Greedy Colouring Bound.
    """
    # Degree order helps the colorer a bit
    deg = {v: len(graph[v]) for v in graph}
    vertices = sorted(graph.keys(), key=lambda v: deg[v], reverse=True)

    max_clique = []
    current = []

    def greedy_coloring_bound(cands):
        """
        Return order(candidates ordered by color) and bound(color indices).
        """
        uncolored = sorted(cands, key=lambda v: deg[v], reverse=True)
        order, bound = [], []
        color = 0 

        while uncolored:
            color += 1
            chosen, remaining = [], []
            for v in uncolored:
                if all(v not in graph[u] for u in chosen):
                    chosen.append(v)
                else:
                    remaining.append(v)
            for v in chosen:
                order.append(v)
                bound.append(color)
            uncolored = remaining

        return order, bound

    def expand(cands):
        nonlocal max_clique

        order, bound = greedy_coloring_bound(cands)

        # Go from most promising to least; prune by color bound
        for i in range(len(order) - 1, -1, -1):
            if len(current) + bound[i] <= len(max_clique):
                return

            v = order[i]
            current.append(v)
            new_cands = cands & graph[v]

            if not new_cands:
                if len(current) > len(max_clique):
                    max_clique = current[:]
            else:
                expand(new_cands)

            current.pop()
            cands.discard(v)

    expand(set(vertices))
    return max_clique

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py <graph_file>")
        sys.exit(1)

    filename = sys.argv[1]
    n, edges = parse_dimacs_graph(filename)

    # Adjacency as sets (fast intersections)
    graph = {i: set() for i in range(1, n + 1)}
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)

    clique = search_max_clique(graph)
    print(f"Maximum clique size: {len(clique)}")
    print(f"Maximum clique: {sorted(clique)}")
"""
Search 2 algorithm with a Greedy Colouring Bound (Etsuji Tomita approach).
A Simple and Faster Branch-and‑Bound Algorithm for Finding a Maximum Clique — Etsuji Tomita et al., 2010. 
https://link.springer.com/content/pdf/10.1007/978-3-642-11440-3_18.pdf?pdf=inline%20link
"""
# Based on the paper above and  the implementation is:
# Conceptually consistent with the MCR (2007) algorithm and the core philosophy of MCS (2010) as
# it uses greedy colouring bounds and ordered exploration,
# but does not include the specific optimisations (Re-NUMBER and Va) introduced.

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
    BnB with Greedy Colouring Bound.
    """
    # Degree order helps the colorer a bit
    deg = {v: len(graph[v]) for v in graph}
    vertices = sorted(graph.keys(), key=lambda v: deg[v], reverse=True)

    max_clique = []
    current = []

    def greedy_colouring_bound(cands):
        """
        Return order(candidates ordered by color) and bound(color indices).
        """
        uncolored = sorted(cands, key=lambda v: deg[v], reverse=True) # order by degree
        order, bound = [], []
        color = 0 

        while uncolored:
            color += 1 # new color
            chosen, remaining = [], []
            for vertex in uncolored:
                if all(vertex not in graph[u] for u in chosen): # can use this color
                    chosen.append(vertex)   # assign color
                else:
                    remaining.append(vertex) # try later
            for vertex in chosen:
                order.append(vertex)
                bound.append(color)
            uncolored = remaining

        return order, bound

    def expand(cands):
        nonlocal max_clique

        order, bound = greedy_colouring_bound(cands)

        # Go from most promising to least --> prune by color bound
        for i in range(len(order) - 1, -1, -1):
            if len(current) + bound[i] <= len(max_clique):
                return

            vertex = order[i]
            current.append(vertex)
            new_cands = cands & graph[vertex]

            # If no candidates left, check for max clique
            if not new_cands:
                if len(current) > len(max_clique):
                    max_clique = current[:]
            else:
                expand(new_cands)

            current.pop() # backtrack
            cands.discard(vertex)

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
"""
Classic improvement to BnB: order the vertices by their degree (most connected first).
Based on: Initial Sorting of Vertices in the Maximum Clique Problem Reviewed — Pablo San Segundo et al., 2014. 
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
    """Branch and Bound algorithm with sorted vertices by degree."""
    vertices = sorted(graph.keys(), key=lambda v: len(graph[v]), reverse=True)
    max_clique = []

    def heuristic(current, remaining):
        # Inefficient heuristic: just use current size + remaining count
        return len(current) + len(remaining)

    def backtrack(current, remaining, depth=0):
        nonlocal max_clique

        if heuristic(current, remaining) <= len(max_clique):
            return # PRUNING

        if len(current) > len(max_clique):
            max_clique = current[:]

        # BRANCH
        for i in range(len(remaining)):
            vertex = remaining[i]

            # Check if the vertex can join the current clique
            can_add = all(neighbor in graph[vertex] for neighbor in current)
            if not can_add:
                continue

            # Compute remaining candidates
            new_remaining = []
            for v in remaining[i + 1:]:
                if all(v in graph[c] for c in current) and v in graph[vertex]:
                    new_remaining.append(v)

            # If the branch can still beat the best clique --> Recursive
            if len(current) + 1 + len(new_remaining) > len(max_clique): # Also considering the vertex that is being added
                backtrack(current + [vertex], new_remaining, depth + 1)

    backtrack([], vertices)
    return max_clique

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py <graph_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    num_vertices, edges = parse_dimacs_graph(filename)
    
    # Convert edges to adjacency list representation
    graph = {i: set() for i in range(1, num_vertices + 1)}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    
    result = search_max_clique(graph)
    print(f"Maximum clique size: {len(result)}")
    print(f"Maximum clique: {sorted(result)}")
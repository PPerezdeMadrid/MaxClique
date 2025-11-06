"""
Removed inefficient heuristic check
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
    """Backtracking + simple Branch and Bound (basic pruning)."""
    vertices = list(graph.keys())
    max_clique = []

    def backtrack(current, remaining, depth=0):
        nonlocal max_clique

        # Basic pruning
        if len(current) + len(remaining) <= len(max_clique):
            return  

        if len(current) > len(max_clique):
            max_clique = current[:]

        # Branching step
        for i in range(len(remaining)):
            vertex = remaining[i]
            if all(neighbor in graph[vertex] for neighbor in current):
                new_remaining = [v for v in remaining[i + 1:] if all(v in graph[c] for c in current)]
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

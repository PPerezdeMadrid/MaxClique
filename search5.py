"""
Instead of using len(remaining), we calculate how many candidates are actually
 connected to everyone in the current clique.
Based on: Reducing the Branching in a Branch and Bound Algorithm for the Maximum Clique Problem — Ciaran McCreesh & Patrick Prosser, 2014.
https://link.springer.com/chapter/10.1007/978-3-319-10428-7_40
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
    """Branch and Bound algorithm with improved bounding step:
    instead of len(remaining), only count vertices connected to all in current clique.
    """
    vertices = sorted(graph.keys(), key=lambda v: len(graph[v]), reverse=True)
    max_clique = []

    def heuristic(current, connected_candidates):
        return len(current) + len(connected_candidates)

    def backtrack(current, remaining, depth=0):
        nonlocal max_clique

        # Only count candidates that are connected to all nodes in the current clique
        connected_candidates = [
            v for v in remaining
            if all(v in graph[u] for u in current)
        ]

        # Pruning: even with all connected candidates, can't beat current max
        if heuristic(current, connected_candidates) <= len(max_clique):
            return

        # Update best clique found
        if len(current) > len(max_clique):
            max_clique = current[:]

        # Branching
        for i in range(len(remaining)):
            vertex = remaining[i]

            # Check if vertex can join the current clique
            if all(neighbor in graph[vertex] for neighbor in current):
                # Compute new remaining candidates
                new_remaining = [
                    v for v in remaining[i + 1:]
                    if v in graph[vertex] and all(v in graph[c] for c in current)
                ]

                # Continue exploring if possible improvement (+1 because we add vertex)
                if len(current) + 1 + len(new_remaining) > len(max_clique):
                    backtrack(current + [vertex], new_remaining, depth + 1)

    backtrack([], vertices)
    return max_clique   # ✅ return added


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

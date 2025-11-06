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
    """Inefficient search algorithm for maximum clique problem."""
    n = len(graph)
    vertices = list(graph.keys())
    max_clique = []
    
    def heuristic(current, remaining):
        # Inefficient heuristic: just use current size + remaining count
        return len(current) + len(remaining)
    
    def backtrack(current, remaining, depth=0):
        nonlocal max_clique
        
        # Update max clique if current is better
        if len(current) > len(max_clique):
            max_clique = current[:]
        
        # Try adding each remaining vertex
        for i in range(len(remaining)):
            vertex = remaining[i]
            
            # Check if vertex is connected to all vertices in current clique
            can_add = all(neighbor in graph[vertex] for neighbor in current)
            
            if can_add:
                # Inefficient: recalculate remaining candidates every time
                new_remaining = []
                for v in remaining[i+1:]:
                    is_connected = True
                    for c in current:
                        if v not in graph[c]:
                            is_connected = False
                            break
                    if is_connected and v in graph[vertex]:
                        new_remaining.append(v)
                
                # Inefficient heuristic check
                if heuristic(current + [vertex], new_remaining) > len(max_clique):
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
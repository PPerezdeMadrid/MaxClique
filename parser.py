import os

def parse_dimacs_graph(filename):
    """
    Parse a DIMACS format graph file.
    
    Returns:
        tuple: (num_vertices, edges) where edges is a set of tuples (u, v)
    """
    num_vertices = 0
    edges = set()
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('c'):
                # Comment line, skip
                continue
            elif line.startswith('p'):
                # Problem line: p FORMAT VERTICES EDGES
                parts = line.split()
                num_vertices = int(parts[2])
            elif line.startswith('e'):
                # Edge line: e vertex1 vertex2
                parts = line.split()
                u = int(parts[1])
                v = int(parts[2])
                
                # Ignore self-loops (same start and end vertex)
                if u != v:
                    edges.add((u, v))
    
    return num_vertices, edges


# Example usage:
# num_vertices, edges = parse_dimacs_graph('C125.9.clq')
# print(f"Graph has {num_vertices} vertices and {len(edges)} edges")

""" Print all .clq files 
 
DIMACS_FOLDER = "DIMACS"
files = [f for f in os.listdir(DIMACS_FOLDER) if f.endswith(".clq")]
files.sort()

print(f"Found {len(files)} graph files in '{DIMACS_FOLDER}':\n")
for file in files:
    path = os.path.join(DIMACS_FOLDER, file)
    n, edges = parse_dimacs_graph(path)
    print(f"{file}: {n} vertices, {len(edges)} edges")

"""
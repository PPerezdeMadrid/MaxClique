import os
import sys
import time
from parser import parse_dimacs_graph
from search import search_max_clique

def run_single_graph(file_name):
    """Run the search algorithm on one graph file"""
    print(f"\nRunning {file_name}...")
    path = os.path.join("DIMACS", file_name)

    # Read graph
    num_vertices, edges = parse_dimacs_graph(path)
    print(f"==> Vertices: {num_vertices}, Edges: {len(edges)}")

    # Build adjacency list
    graph = {i: set() for i in range(1, num_vertices + 1)}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    # Run the search
    start = time.time()
    result = search_max_clique(graph)
    end = time.time()

    print(f"==> Max clique size: {len(result)}")
    print(f"==> Max clique: {sorted(result)}")
    print(f"==> Time: {end - start:.3f} s")

def main():
    # If a specific graph is passed
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        run_single_graph(file_name)
    else:
        # If no argument, run all .clq files in DIMACS folder
        print("No file provided. Running all .clq files in DIMACS folder...\n")
        files = [f for f in os.listdir("DIMACS") if f.endswith(".clq")]
        files.sort()

        if not files:
            print("No .clq files found in DIMACS folder.")
            sys.exit(1)

        for f in files:
            run_single_graph(f)

    print("\nAll graphs done.")

if __name__ == "__main__":
    main()

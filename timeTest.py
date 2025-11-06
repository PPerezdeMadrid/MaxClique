import importlib
import time
import csv
import os
import sys
from parser import parse_dimacs_graph

# List of search versions to compare
VERSIONS = ["search", "search2", "search3", "search4", "search5"]
DIMACS_FOLDER = "DIMACS"
OUTPUT_FILE = "results.csv"

# johnson8-2-4.clq and p_hat300-1.clq ==> small instances

def load_graph(file_name):
    """Reads the DIMACS file and builds the graph"""
    path = os.path.join(DIMACS_FOLDER, file_name)
    num_vertices, edges = parse_dimacs_graph(path)
    graph = {i: set() for i in range(1, num_vertices + 1)}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    return graph

def run_version(module_name, graph):
    """Runs one version of search and returns time + clique size"""
    mod = importlib.import_module(module_name)
    func = getattr(mod, "search_max_clique")
    start = time.time()
    result = func(graph)
    end = time.time()
    return end - start, len(result)

def test_one_graph(graph_file):
    """Runs all search versions on one graph"""
    print(f"\nTesting {graph_file}...")
    graph = load_graph(graph_file)
    results = {"File": graph_file}

    for version in VERSIONS:
        print(f"Running {version}...")
        try:
            t, size = run_version(version, graph)
            results[version] = round(t, 3)
            print(f"     ==> time = {t:.3f}s, clique size = {size}")
        except Exception as e:
            print(f"     ==> error running {version}: {e}")
            results[version] = "error"

    # Write to CSV
    write_header = not os.path.exists(OUTPUT_FILE)
    with open(OUTPUT_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["File"] + VERSIONS)
        if write_header:
            writer.writeheader()
        writer.writerow(results)

    print(f"Saved results for {graph_file}")

def main():
    # If a specific graph is given, test just that one
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        test_one_graph(file_name)
    else:
        # Otherwise, test all .clq files in DIMACS folder
        print("No file given, testing all .clq graphs in DIMACS...\n")
        graphs = [f for f in os.listdir(DIMACS_FOLDER) if f.endswith(".clq")]
        graphs.sort()

        if not graphs:
            print("No .clq files found in DIMACS folder.")
            sys.exit(1)

        for g in graphs:
            test_one_graph(g)

    print("\nAll tests finished.")

if __name__ == "__main__":
    main()

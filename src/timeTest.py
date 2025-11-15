import importlib
import time
import csv
import os
import sys
from parser import parse_dimacs_graph
import matplotlib.pyplot as plt
import multiprocessing

# List of search versions to compare
VERSIONS = ["search", "search2", "search3", "search4"]
DIMACS_FOLDER = "../DIMACS"
OUTPUT_FILE = "results.csv"
PLOTS_DIR = "plots" 

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


def _worker(func, graph, return_dict):
    """Internal worker that runs the search algorithm in a separate process."""
    try:
        result = func(graph)
        return_dict["result"] = result
        return_dict["error"] = None
    except Exception as e:
        return_dict["result"] = None
        return_dict["error"] = str(e)

def run_version(module_name, graph, timeout=600):
    """
    Runs one version of search inside a separate process.
    If it takes longer than 'timeout' seconds (default: 10 minutes),
    it will be terminated and recorded as a timeout.
    """
    mod = importlib.import_module(module_name)
    func = getattr(mod, "search_max_clique")

    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    p = multiprocessing.Process(target=_worker, args=(func, graph, return_dict))
    start = time.time()
    p.start()
    p.join(timeout)

    if p.is_alive():
        # Timeout happened --> kill the process
        p.terminate()
        p.join()
        return "timeout", None 

    end = time.time()

    if return_dict.get("error") is not None:
        # Error raised inside the worker
        return "error", None

    result = return_dict.get("result")
    if result is None:
        return "error", None

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

            # If timeout or error, store the string directly
            if isinstance(t, (int, float)):
                results[version] = round(t, 3)
                print(f"     ==> time = {t:.3f}s, clique size = {size}")
            else:
                results[version] = t  # "timeout" or "error"
                print(f"     ==> time = {t}, clique size = {size}")

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

# Code for generating plots from results.csv
def _safe_float(v):
    try:
        return float(v)
    except:
        return None

def _ensure_plots_dir():
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR, exist_ok=True)

def generate_plots_from_csv(csv_path=OUTPUT_FILE):
    """Reads results.csv and generates PNG plots into plots/"""
    if not os.path.exists(csv_path):
        print(f"[plot] No CSV found at {csv_path}; skipping plots.")
        return

    _ensure_plots_dir()

    # Read all rows
    rows = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    if not rows:
        print("[plot] CSV is empty; skipping plots.")
        return

    # --- Per-file bar charts ---
    for r in rows:
        file_name = r["File"]
        times = [_safe_float(r.get(v)) for v in VERSIONS]
        labels = []
        values = []
        for lab, val in zip(VERSIONS, times):
            if val is not None:
                labels.append(lab)
                values.append(val)

        if not values:
            continue  # all errors

        plt.figure()
        plt.bar(labels, values)
        plt.ylabel("Time (s)")
        plt.title(f"Runtime by Version — {file_name}")
        plt.tight_layout()
        out_path = os.path.join(PLOTS_DIR, f"{os.path.splitext(file_name)[0]}_times.png")
        plt.savefig(out_path, dpi=150)
        plt.close()
        print(f"[plot] Saved {out_path}")

    # --- Overall average per version ---
    sums = {v: 0.0 for v in VERSIONS}
    counts = {v: 0 for v in VERSIONS}
    for r in rows:
        for v in VERSIONS:
            val = _safe_float(r.get(v))
            if val is not None:
                sums[v] += val
                counts[v] += 1
    avg_labels = []
    avg_vals = []
    for v in VERSIONS:
        if counts[v] > 0:
            avg_labels.append(v)
            avg_vals.append(sums[v] / counts[v])

    if avg_vals:
        plt.figure()
        plt.bar(avg_labels, avg_vals)
        plt.ylabel("Average Time (s)")
        plt.title("Average Runtime by Version (across all instances)")
        plt.tight_layout()
        out_path = os.path.join(PLOTS_DIR, "overall_avg_times.png")
        plt.savefig(out_path, dpi=150)
        plt.close()
        print(f"[plot] Saved {out_path}")
    else:
        print("[plot] No valid numeric data to compute averages.")
# ------------- End of plot code -------------

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
            
        print("\nGenerating plots...")
        generate_plots_from_csv(OUTPUT_FILE)
        print("Plots finished.")

    print("\nAll tests finished.")

if __name__ == "__main__":
    main()

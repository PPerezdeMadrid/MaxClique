"""
Code generated to visualize graphs from DIMACS files using NetworkX and Matplotlib.
"""

import os
import sys
import matplotlib.pyplot as plt
import networkx as nx
from parser import parse_dimacs_graph

DIMACS_FOLDER = "../DIMACS"

def load_graph(file_name):
    """Reads a DIMACS file and returns a NetworkX graph"""
    path = os.path.join(DIMACS_FOLDER, file_name)
    num_vertices, edges = parse_dimacs_graph(path)

    G = nx.Graph()
    G.add_nodes_from(range(1, num_vertices + 1))
    G.add_edges_from(edges)
    return G

def visualize_graph(G, title):
    """Displays the graph using matplotlib"""
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(G, seed=42)  # nicer layout
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color="skyblue")
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title(title)
    plt.axis("off")
    plt.show()

def main():
    # Check input
    if len(sys.argv) < 2:
        print("Usage: python visualizeGraphs.py <graph_file>")
        print("Example: python visualizeGraphs.py hamming6-2.clq")
        sys.exit(1)

    file_name = sys.argv[1]
    print(f"Loading graph {file_name}...")
    G = load_graph(file_name)
    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    visualize_graph(G, f"{file_name} ({G.number_of_nodes()} nodes)")

if __name__ == "__main__":
    main()

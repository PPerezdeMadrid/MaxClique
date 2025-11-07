"""
Search 2 algorithm with a Greedy Colouring Bound (Etsuji Tomita approach).
A Simple and Faster Branch-and‑Bound Algorithm for Finding a Maximum Clique — Etsuji Tomita et al., 2010. 
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
    """
    Branch & Bound con cota de coloración greedy (tipo Tomita/MCQ).
    Suele ser notablemente más rápido que un B&B con poda len(current)+len(remaining).
    """
    # Precompute grados para ordenar y para el colorista
    deg = {v: len(graph[v]) for v in graph}
    vertices = sorted(graph.keys(), key=lambda v: deg[v], reverse=True)

    max_clique = []
    current = []

    def greedy_coloring_bound(cand_set):
        """
        Devuelve:
          - order: lista de candidatos en el orden en que se colorean
          - bound: bound[i] = color asignado a order[i] (nº de color, 1..k)
        Construcción por capas: cada 'color' es un MIS (conjunto independiente) greedy.
        """
        # Lista de nodos a colorear, ordenados por grado para acelerar
        uncolored = sorted(cand_set, key=lambda v: deg[v], reverse=True)
        order, bound = [], []
        color = 0

        # Para cada color, construimos un conjunto independiente maximal greedy
        while uncolored:
            color += 1
            chosen = []
            remaining = []
            # Escogemos nodos que no choquen con los ya elegidos en este color
            for v in uncolored:
                if all((v not in graph[u]) for u in chosen):
                    chosen.append(v)
                else:
                    remaining.append(v)
            # Asignamos este color a los 'chosen'
            for v in chosen:
                order.append(v)
                bound.append(color)
            # Continuamos con los que quedaron sin colorear
            uncolored = remaining

        return order, bound

    def expand(cand_set):
        nonlocal max_clique

        # Cota superior por coloración (muy efectiva para podar)
        order, bound = greedy_coloring_bound(cand_set)

        # Recorremos en orden inverso (más prometedor primero).
        # Si len(current) + bound[i] <= len(max_clique), podemos cortar el resto.
        for i in range(len(order) - 1, -1, -1):
            if len(current) + bound[i] <= len(max_clique):
                return  # poda por cota de coloración

            v = order[i]
            current.append(v)

            # Nuevos candidatos = vecinos de v dentro de cand_set
            new_cand = cand_set & graph[v]

            if not new_cand:
                # Hoja: actualiza máximo si mejora
                if len(current) > len(max_clique):
                    max_clique = current[:]
            else:
                expand(new_cand)

            current.pop()
            # Eliminamos v de candidatos globales para no reexpandirlo
            cand_set.discard(v)

    expand(set(vertices))
    return max_clique

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py <graph_file>")
        sys.exit(1)

    filename = sys.argv[1]
    num_vertices, edges = parse_dimacs_graph(filename)

    # Convert edges to adjacency list representation (sets para intersecciones rápidas)
    graph = {i: set() for i in range(1, num_vertices + 1)}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    result = search_max_clique(graph)
    print(f"Maximum clique size: {len(result)}")
    print(f"Maximum clique: {sorted(result)}")

¡De una! Te dejo un README listo para pegar (en inglés sencillo, estilo británico) y, al final, una mejora concreta y autocontenida para el algoritmo básico de `src/search.py` (branch & bound con acotación por coloreo voraz). Si quieres, puedo volcarlo a un archivo después.

---

# MaxClique — Branch & Bound Playground

A small toolkit to experiment with Maximum Clique algorithms on DIMACS graphs.
It includes a very simple baseline (`search.py`) and several faster variants (`search2.py`, `search3.py`, `search4.py`), plus scripts to benchmark, plot, and visualise results.

## Folder layout

```
DIMACS/                 # Graph instances (.clq)
doc/                    # Notes / exported HTML/PDF
src/
  main.py               # CLI entry point
  parser.py             # DIMACS reader
  search.py             # Basic baseline (to be improved)
  search2.py            # Baseline-compatible, more complete
  search3.py            # Faster variant
  search4.py            # Another variant / idea
  visualizeGraphs.py    # Simple graph viewer
  timeTest.py           # Batch benchmark runner
  plots/                # Plot helpers
  results.csv           # Collected results (appended by scripts)
  requirements.txt      # Python deps
MCExample.png           # Small example figure
Practical.pdf/html      # Coursework brief
APUNTES.md              # Personal notes
README.md               # This file
```

## What is the Maximum Clique problem?

Given an undirected graph (G=(V,E)), find the largest set of vertices where every pair is connected (a *clique*).
The problem is NP-hard, so we use exact search with good pruning.

## Algorithms included

* **`search.py` — Basic backtracking**
  Straightforward depth-first search that grows a partial clique and tries candidates. Good to read first, but slow on medium graphs.

* **`search2.py` — Complete baseline**
  Same interface as `search.py`, but with a proper upper bound so it matches the true optimum on all instances used here.

* **`search3.py`, `search4.py` — Faster ideas**
  Additional pruning and ordering (e.g., greedy colouring, pivoting, better candidate ordering). Often much faster.

## Install

Tested with Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r src/requirements.txt
```

## Quick start

Run a single instance:

```bash
python src/main.py DIMACS/brock200_2.clq --algo search
# try: --algo search2 | search3 | search4
```

> Tip: `python src/main.py --help` to see available flags in your local version.

Batch benchmark (writes/extends `src/results.csv`):

```bash
python src/timeTest.py
```

Plot or inspect results:

```bash
python src/visualizeGraphs.py
python src/plots/<some_plot_script>.py
```

## Input format

We use classic **DIMACS `.clq`** graphs. `src/parser.py` reads them into an adjacency-set dictionary:

```python
graph[v] -> set of neighbours of v
```

This makes membership tests and intersections fast.

## Output

* CLI prints the **maximum clique size** and **runtime**.
* Batch runs append to **`src/results.csv`** (instance name, algorithm, time, clique size).
* Plots/figures go into `src/plots/` or the working directory depending on the script.

## Reproducibility tips

* Close other heavy apps; some graphs are sensitive to CPU throttling.
* Use the same Python version and dependencies as in `requirements.txt`.
* For fair comparisons, run each algorithm on the same machine/config.

## References (useful starting points)

* E. **Tomita** et al. (2010) — A simple and faster Branch-and-Bound for Maximum Clique
* P. **San Segundo** et al. (2014) — Initial vertex ordering for Maximum Clique
* C. **McCreesh** & P. **Prosser** (2014) — Reducing branching in B&B for Maximum Clique

---

## Suggested improvement to `src/search.py` (drop-in, still simple)

This keeps your basic structure and signature (`search_max_clique(graph)`) but adds:

* **Greedy colouring bound** to cap the best possible extension from the current node.
* **Candidate ordering** by colour (cheap and effective).
* **Adjacency-set** intersections for fast filtering.

It’s a compact branch-and-bound that remains easy to read and usually gives a *big* speed-up while staying much simpler than state-of-the-art codes.

> Replace the contents of `src/search.py` with the snippet below (or adapt just the core functions).

```python
# src/search.py
# Baseline branch & bound with a greedy-colouring upper bound.
# Keeps the public entrypoint: search_max_clique(graph) -> list of vertices

from typing import Dict, List, Set

Graph = Dict[int, Set[int]]

def _greedy_colouring_bound(vertices: List[int], graph: Graph) -> List[int]:
    """
    Colour 'vertices' with a simple greedy layering:
    returns 'col', where col[i] is the colour index (1..k) for vertices[i].
    The max colour used is an upper bound on the clique size within 'vertices'.
    We return the per-vertex colours so the caller can order by non-increasing colour.
    """
    colours: List[int] = [0] * len(vertices)
    # Each layer is a set of vertices that are pairwise non-adjacent (independent set)
    layers: List[Set[int]] = []  # store vertex indices (positions in 'vertices')

    for i, v in enumerate(vertices):
        placed = False
        for c, layer in enumerate(layers, start=1):
            # Check if 'v' is non-adjacent to all vertices already in this colour layer
            if all(vertices[j] not in graph[v] for j in layer):
                colours[i] = c
                layer.add(i)
                placed = True
                break
        if not placed:
            colours[i] = len(layers) + 1
            layers.append({i})
    return colours

def search_max_clique(graph: Graph) -> List[int]:
    """
    Exact maximum clique with branch & bound using a greedy-colouring upper bound.
    Returns the vertices of one maximum clique (as they appear in 'graph').
    """
    # Work with a stable list of vertices to keep ordering deterministic
    V: List[int] = list(graph.keys())
    # Optional: sort by descending degree to help colouring/pruning
    V.sort(key=lambda v: -len(graph[v]))

    best_clique: List[int] = []

    def expand(current: List[int], candidates: List[int]) -> None:
        nonlocal best_clique
        if not candidates:
            if len(current) > len(best_clique):
                best_clique = current.copy()
            return

        # Upper bound via greedy colouring (fast, order-agnostic)
        colours = _greedy_colouring_bound(candidates, graph)

        # Explore in an order that tries "promising" vertices first:
        # sort by decreasing colour (higher colour -> potentially tighter bound)
        order = sorted(range(len(candidates)), key=lambda i: -colours[i])

        for idx_pos, i in enumerate(order):
            # Prune if even taking the best possible (current + max possible from here)
            # cannot beat the incumbent.
            # Max remaining clique size from this branch <= colours[i]
            if len(current) + colours[i] <= len(best_clique):
                # Since 'order' is by non-increasing colour, we can stop here.
                return

            v = candidates[i]

            # Filter next candidates to those adjacent to 'v' and also *after* i
            # (branch-and-reduce; skipping vertices already considered in this layer)
            next_cands: List[int] = []
            for j in order[idx_pos + 1:]:
                u = candidates[j]
                if u in graph[v]:  # adjacency-set membership (O(1) avg)
                    next_cands.append(u)

            current.append(v)
            expand(current, next_cands)
            current.pop()

            # Optional: early stop if we already hit the theoretical max
            # (cannot do better than current incumbent bound in this subtree)

    expand([], V)
    return best_clique
```

### Why this helps

* **Colour bound**: the number of colours in any greedy colouring of the candidate set is an **upper bound** on the size of any clique inside it. If `|current| + bound ≤ |best|`, we prune the branch.
* **Ordering by colour**: exploring higher-colour vertices first tends to find big cliques early, which tightens the incumbent and triggers more pruning later.
* **Sets everywhere**: `graph[v]` is a `set`, so `u in graph[v]` is fast.

### Keeping behaviour compatible

* The public function remains `search_max_clique(graph) -> List[int]`.
* It returns **one** max clique’s vertex list (not only its size), so your existing driver can still do `len(search_max_clique(graph))`.

---

## Contributing / extending

* Add a new file `src/searchX.py` with a function `search_max_clique(graph)`.
* Import/select it in `src/main.py` via a flag (e.g., `--algo searchX`).
* For speed, consider:

  * static ordering (degree or degeneracy),
  * Tomita-style **pivoting**,
  * improved greedy colouring with recolouring,
  * bitsets (if you need C-speed in pure Python, try `python-bitarray`).

---

If quieres, te lo convierto ahora mismo en `README.md` y también te dejo el `search.py` mejorado como archivo listo para ejecutar.

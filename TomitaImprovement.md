# Maximum Clique: Branch & Bound with a Greedy Colouring Bound

## Core idea

We keep a **current clique** we’re building, and a set of **candidates** that could extend it.
Before exploring deeper, we estimate the **best possible** clique we could still make from those candidates. If that upper bound can’t beat the best solution we already have, we **stop** exploring that branch.

The bound comes from a **greedy graph colouring**: the number of colours used is an upper limit on how big a clique can be inside those candidates.

## Data structures

* The graph is stored as **sets of neighbours**: `graph[v]` is a `set`.
  This makes checks like `u in graph[v]` and intersections `cand & graph[v]` fast.
* Candidates are kept as a **set** too, for the same reason.


## How the greedy colouring bound works

We colour the candidate vertices in simple greedy layers. Each “colour” is a set of vertices with **no edges between them** (an independent set). We keep making such layers until all candidates are coloured.

* The **number of colours** used is our **upper bound**: you can’t get a clique larger than that from the remaining candidates.
* We also keep the **order** in which vertices were coloured and the colour index for each one. We expand vertices in **reverse colour order** (the most “difficult” ones first), which usually triggers pruning earlier.

**Sketch:**

```text
uncoloured ← candidates, sorted by degree (high to low)
order ← [], bound ← []
colour ← 0
while uncoloured not empty:
    colour ← colour + 1
    chosen ← []        # vertices for this colour (independent set)
    remaining ← []
    for v in uncoloured:
        if v has no edge to any u in chosen:
            chosen.append(v)
        else:
            remaining.append(v)
    for v in chosen:
        order.append(v)
        bound.append(colour)
    uncoloured ← remaining
```

## The search (expand)

1. Compute the colouring on the current candidates → `order`, `bound`.
2. Go through `order` **from the end to the start** (reverse colour order).
3. **Prune** if:

   ```
   len(current) + bound[i] <= len(max_clique)
   ```

   No point going deeper; we can’t beat what we’ve got.
4. Otherwise:

   * Add the vertex `v` to `current`.
   * Build new candidates with a fast set intersection:

     ```python
     new_cand = cand_set & graph[v]
     ```
   * If `new_cand` is empty, we’ve reached a **maximal clique** — update `max_clique` if it’s larger.
   * Backtrack: remove `v` from `current`, and `discard` it from the candidate set so we don’t revisit it.


## Why it’s fast

* **Tight upper bound:** the greedy colouring gives a much better upper bound than “current size + remaining count”, so we prune far more branches.
* **Good ordering:** processing vertices in reverse colouring order tends to hit dead ends (and prune) sooner.
* **Set math:** using `set` intersections is much faster than nested loops.


## Pseudocode

```text
search_max_clique(G):
    deg[v] = degree of v
    vertices = V sorted by degree descending
    max_clique = []
    current = []

    function greedy_colouring_bound(C):
        uncoloured = C sorted by degree descending
        order, bound = [], []
        colour = 0
        while uncoloured:
            colour += 1
            chosen, remaining = [], []
            for v in uncoloured:
                if v has no edge to any u in chosen:
                    chosen.append(v)
                else:
                    remaining.append(v)
            for v in chosen:
                order.append(v)
                bound.append(colour)
            uncoloured = remaining
        return order, bound

    function expand(C):
        order, bound = greedy_colouring_bound(C)
        for i from len(order)-1 down to 0:
            if len(current) + bound[i] <= len(max_clique):
                return
            v = order[i]
            current.push(v)
            newC = C ∩ N(v)
            if newC is empty:
                if len(current) > len(max_clique):
                    max_clique = current.copy()
            else:
                expand(newC)
            current.pop()
            C.remove(v)

    expand(set(vertices))
    return max_clique
```


## Correctness

* We only ever add vertices that are **adjacent to all** in `current`, so `current` stays a clique.
* The colouring bound is a **valid upper bound**, so pruning never removes an optimal solution.
* When candidates run out, `current` is maximal; we keep the largest found.


## Practical results (your run)

| Algorithm                | Time on `MANN_a9.clq` | Clique size |
| ------------------------ | --------------------: | ----------: |
| `search`                 |              21.273 s |          16 |
| `search2`                |               7.730 s |          16 |
| `search3` (this version) |           **0.002 s** |          16 |

**In short:** the greedy colouring bound and set-based filtering do the heavy lifting.
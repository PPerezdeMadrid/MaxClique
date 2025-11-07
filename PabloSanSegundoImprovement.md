# Maximum Clique: Branch & Bound with Initial Degree Ordering (search2)

This is a simple write-up of the **search2** version where we add **initial vertex ordering by degree (high to low)**. Everything else stays the same as your original `search2`, so you can measure the effect of ordering alone.


## Goal

Find the **maximum clique** in a graph using **backtracking (Branch & Bound)**.
We keep the same pruning rule as before and only change the **starting order of vertices**.


## What changed

* **New step:** before the search starts, sort all vertices by **degree descending** (most connected first).
* All other parts (pruning, recursion, candidate building) are **unchanged** from your `search2`.

Why degree first? Highly connected vertices are more likely to form large cliques. Exploring them early often helps the bound cut more branches.


## Data structures

* Graph stored as **sets of neighbours**: fast `in` checks and set logic.
* Candidate lists kept as **Python lists** inside the recursion to preserve the chosen order.


## Pruning rule (same as before)

We use a very simple upper bound:

```
bound = len(current) + len(remaining)
```

If this bound is **not greater** than the best clique found so far, we **stop** exploring that branch.


## Algorithm steps

1. **Preprocess**

   * Compute the degree of each vertex.
   * Sort vertices by degree (high → low). This is our initial order.

2. **Backtrack**

   * Update the best clique if `current` is larger.
   * If `len(current) + len(remaining) <= len(max_clique)`, prune.
   * For each vertex `v` in `remaining` (in the sorted order):

     * Check `v` is connected to all in `current`.
     * Build `new_remaining` = vertices after `v` that are connected to **all** of `current` **and** to `v`.
     * Optional local prune (same as your code): if `len(current)+1 + len(new_remaining) <= len(max_clique)`, return.
     * Recurse with `current + [v]` and `new_remaining`.

3. **Finish**

   * Return the largest clique recorded.


## Pseudocode (high level)

```text
search_max_clique(G):
    deg[v] = |N(v)|
    vertices = sort V by deg[v] descending
    max_clique = []

    function heuristic(current, remaining):
        return len(current) + len(remaining)

    function backtrack(current, remaining):
        if len(current) > len(max_clique):
            max_clique = copy(current)

        if heuristic(current, remaining) <= len(max_clique):
            return

        for i in 0..len(remaining)-1:
            v = remaining[i]
            if v is adjacent to all in current:
                new_remaining = []
                for u in remaining[i+1:]:
                    if u is adjacent to all in current and to v:
                        new_remaining.append(u)

                if heuristic(current+[v], new_remaining) <= len(max_clique):
                    return  # same behaviour as your original search2

                backtrack(current+[v], new_remaining)

    backtrack([], vertices)
    return max_clique
```


## Why this helps

* Starting from **high-degree** vertices often reaches **large cliques earlier**.
* Finding a good clique early **raises the bar** for pruning, so later branches get cut sooner.
* The colouring bound is not used here; the gain comes purely from **better initial order**.


## Limitations

* The bound `len(current) + len(remaining)` is **weak** on many graphs.
* Degree ordering is good but **not always best**. Some graphs prefer other orderings (e.g., degeneracy on sparse graphs, or colour-based orders).



# Maximum Clique: Branch & Bound with Initial Degree Ordering

This is a simple write-up of the search2 version where it is added initial vertex ordering by degree (high to low).


## Goal

Find the maximum clique in a graph. The same pruning rule as before is used, and only the starting order of the vertices is changed.


## What changed

* New step: before the search starts, sort all vertices by degree descending (most connected first).
* All other parts (pruning, recursion, candidate building) are unchanged from the `search2`.

Why degree first? Highly connected vertices are more likely to form large cliques. Exploring them early often helps the bound cut more branches.

## Algorithm steps

1. **Preprocess**

   * Compute the degree of each vertex.
   * Sort vertices by degree (high → low). This the initial order.

2. **Backtrack**

   * Update the best clique if `current` is larger.
   * If `len(current) + len(remaining) <= len(max_clique)`, prune.
   * For each vertex `v` in `remaining` (in the sorted order):

     * Check `v` is connected to all in `current`.
     * Build `new_remaining` = vertices after `v` that are connected to all of `current` and to `v`.
     * Same local pruning as in `search 2`.
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

* Starting from high-degree vertices often reaches large cliques earlier.
* Finding a good clique early raises the bar for pruning, so later branches get cut sooner.



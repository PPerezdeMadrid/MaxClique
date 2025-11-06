Empezamos con un algoritmo que tiene:
- Una heurística ineficiente
- Y que hace bactracking puro, va revisando cada nodo uno por uno
- La heurística no distingue ramas “buenas” de “malas”.

1) Cambio que hago es añadir una forma de podar las ramas (implementaré BnB)
antes de entrar en el bucle de vértices, añadimos una verificación tipo “bound”:

Si el tamaño máximo posible de esta rama ≤ tamaño del mejor clique → corta.

```python
if len(current) + len(remaining) <= len(max_clique):
    return  # prune branch
```



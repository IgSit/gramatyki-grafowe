# GRAMATYKI GRAFOWE PROJEKT 2
### Wymagania:
`Python 3.12`

### Jak uruchomić:
`pip install -r requirements.txt`
`python ./main.py`

### Jak używać:

- Nazwy wierzchołków są ich id, więc muszą być unikatowe. 
- Konwencja jest taka że muszą to być stringi.
- Atrybuty podajemy w słowniku w tej samej krotce, atrybut `'pos': tuple[float, float]` (współrzędne) jest wymagany dla node.
- Nazwa X* jest zarezerwowana dla generycznych wierzchołków zastępujących hiperkrawędzie.

Konstrukcja przykładowego hipergrafu:
```
hyper_graph1 = HyperGraph(
    nodes=[
        ('v1', {'pos': (0, 0), 'h': False}),
        ('v2', {'pos': (4, 0), 'h': False}),
        ('v3', {'pos': (4, 4), 'h': False}),
        ('v4', {'pos': (0, 4), 'h': False}),
        ('v5', {'pos': (4, 2), 'h': True})
    ],
    edges=[
        ({'v1', 'v2'}, {'label': 'E', 'B': True}),
        ({'v2', 'v5'}, {'label': 'E', 'B': True}),
        ({'v5', 'v3'}, {'label': 'E', 'B': True}),
        ({'v3', 'v4'}, {'label': 'E', 'B': True}),
        ({'v4', 'v1'}, {'label': 'E', 'B': True}),
        ({'v1', 'v2', 'v3', 'v4'}, {'label': 'Q', 'R': True})
    ]
)
```

- HyperGraph ma metody `extend(nodes, edges)` oraz `shrink(nodes, edges)`, odpowiednio dodają i usuwają elementy grafu. Uwaga: ta pierwsza wymaga słownika atrybutów (nawet pustego), ta druga już tylko samych id.
- Metoda `visualize()` rysuje graf.
- Pole `graph.nx_graph` daje dostęp do reprezentacji w networkx. READ ONLY. Nie wolno przeprowadzać modyfikacji bezpośrednio na tym obiekcie, ponieważ wprowadzi to różnice względem innych kolekcji obiektu.

### Produkcje
Każdą produkcję umieszczamy w dedykowanym pliku w katalogu productions.
Należy dziedziczyć po abstrakcyjnej klasie `Production` i zaimplementować `check(graph, node)` oraz `apply(graph, node)`.


### Testy
Testy umieszczamy w katalogu tests.



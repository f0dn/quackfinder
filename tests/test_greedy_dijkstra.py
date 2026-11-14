import networkx as nx
from quackfinder.implementation import dijkstra
import pytest


case1_edges = [
    ('A', 'B', 3),
    ('A', 'D', 5),
    ('B', 'C', 7),
    ('D', 'C', 3),
    ('C', 'E', 2),
    ('D', 'F', 1),
    ('F', 'E', 3),
]

case2_edges = [
    ('A', 'B', 4),
]

case3_edges = [
    ('A', 'B', 1),
    ('B', 'D', 20),
    ('A', 'C', 4),
    ('C', 'D', 2),
]

case4_edges = [
    ('A', 'B', 2),
]

case5_edges = [
    (1, 2, 2),
    (2, 3, 2),
    (3, 4, 2),
    (1, 4, 7),
]

case6_edges = [
    ('S', 'A', 2),
    ('S', 'B', 2),
    ('A', 'C', 3),
    ('B', 'C', 1),
    ('C', 'T', 4),
    ('A', 'T', 9),
]


@pytest.mark.parametrize(
    "edges, expected, start_node, end_node",
    [
        (case1_edges, 12, 'A', 'E'),   # Case 1
        (case2_edges, 4, 'A', 'B'),   # Case 2
        (case3_edges, 21, 'A', 'D'),   # Case 3
        (case4_edges, 0, 'A', 'A'),   # Case 4
        (case5_edges, 6, 1, 4),       # Case 5
        (case6_edges, 7, 'S', 'T'),   # Case 6
    ]
)
def test_dijkstra(edges, expected, start_node, end_node):
    G = nx.DiGraph()

    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])

    assert dijkstra(G, start_node, end_node)[1] == expected

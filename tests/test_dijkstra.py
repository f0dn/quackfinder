import networkx as nx
from quackfinder.implementation import dijkstra
import pytest

case1_edges = [
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 1),
    ('B', 'D', 5),
    ('C', 'D', 8),
    ('C', 'E', 10),
    ('D', 'E', 2),
]

@pytest.mark.parametrize(
    "edges, expected, start_node, end_node",
    [
        (case1_edges, 11, 'A', 'E'),
        (case1_edges, 10, 'C', 'E'),
    ]
)
def test_dijkstra(edges, expected, start_node, end_node):
    G = nx.DiGraph()

    for edge in edges:
        G.add_edge(edge[0], edge[1], edge_weight=edge[2])

    assert dijkstra(G, start_node, end_node) == expected

import networkx as nx


def test():
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4, 5])
    list = [(1, 2, 3), (2, 3, 7), (3, 5, 2), (1, 4, 5), (4, 5, 1)]
    for i in list:
        G.add_weighted_edges_from(i)

    # G.add_weighted_edges_from([(1, 2, 3)], [2, 3, 7], [3, 5, 2], [1, 4, 5], [4,5,1])

    print(dijkstra(G))


def dijkstra(G):
    print("Hello")


test()

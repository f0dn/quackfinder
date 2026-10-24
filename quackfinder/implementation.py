import networkx as nx

def test():
    G = nx.Graph()
    # G.add_nodes_from([1, 2, 3, 4, 5])
    # list = [(1, 2, 3), (2, 3, 7), (3, 5, 2), (1, 4, 5), (4, 5, 1)]
    # for i in list:
    #     G.add_weighted_edges_from(i)

    G.add_edge('A', 'B', weight=3)
    G.add_edge('B', 'C', weight=7)
    G.add_edge('C', 'E', weight=2)
    G.add_edge('A', 'D', weight=5)
    G.add_edge('D', 'F', weight=1)

    print(dijkstra(G))

def dijkstra(G):
    print("Hello")
    print(G.edges)

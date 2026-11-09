import networkx as nx


def test():
    G = nx.DiGraph()

    G.add_edge('A', 'B', weight=3)
    G.add_edge('A', 'D', weight=5)
    G.add_edge('B', 'C', weight=7)
    G.add_edge('D', 'C', weight=3)
    G.add_edge('C', 'E', weight=2)
    G.add_edge('D', 'F', weight=1)
    G.add_edge('F', 'E', weight=3)

    print(dijkstra(G, "A", "E"))


def closest_neighbor(G, starting_node):
    closest_node = ""
    for node in G.neighbors(starting_node):
        if closest_node == "":
            closest_node = node
        else:
            if G.get_edge_data(starting_node, node)['weight'] <= G.get_edge_data(starting_node, closest_node)['weight']:
                closest_node = node
        # print(node)
    return (closest_node, G.get_edge_data(starting_node, closest_node)['weight'])


def dijkstra(G, starting_node, ending_node):
    total_distance = 0
    final_path = [starting_node]
    current_node = starting_node

    # final_path.append("TESTING")
    # print(final_path[-1])

    while final_path[-1] != ending_node:
        closest_neighbor(G, current_node)
        data = closest_neighbor(G, current_node)
        final_path.append(data[0])
        total_distance += data[1]
        current_node = data[0]

    return final_path, total_distance


test()

import networkx as nx
import math
import heapq

INFTY = math.inf

def test():
    G = nx.DiGraph()

    G.add_edge('A', 'B', edge_weight=3)
    G.add_edge('A', 'D', edge_weight=5)
    G.add_edge('B', 'C', edge_weight=7)
    G.add_edge('D', 'C', edge_weight=3)
    G.add_edge('C', 'E', edge_weight=2)
    G.add_edge('D', 'F', edge_weight=1)
    G.add_edge('F', 'E', edge_weight=3)

    print(dijkstra(G, "A", "E"))

def iterative_step(G):

    # STEP 1: choose the node with the smallest node_weight
    current_node = "" # node with the smallest node_weight
    for (node,node_data) in G.nodes(data=True):
        # don't even consider them if they have already been visited
        if node_data["visited"] == False:
            if current_node == "": # only happens in the first loop cycle
                current_node = node
            else:
                if node_data["node_weight"] <= G.nodes[current_node]["node_weight"]:
                    current_node = node
    # print(current_node)

    # STEP 2: visit its neighbors
    data = G.nodes(data=True)
    
    for neighbor in G.neighbors(current_node):
        if not data[neighbor]["visited"]:
            # print(f"NBR: {neighbor}")
            # print("---")
            new_cumulative_sum = data[current_node]["node_weight"] + G.get_edge_data(current_node, neighbor)["edge_weight"]
            if (new_cumulative_sum) <= data[neighbor]["node_weight"]:
                data[neighbor]["node_weight"] = new_cumulative_sum
    G.nodes[current_node]["visited"] = True

def dijkstra(G, starting_node, ending_node):
    G.nodes[starting_node]["node_weight"] = 0
    for (node,node_data) in G.nodes(data=True):
        node_data["visited"] = False
        if node != starting_node:
            node_data["node_weight"] = INFTY
        # print(f"{node}, {node_data}")

    number_of_visited_nodes = 0
    while number_of_visited_nodes != len(G.nodes): 
        iterative_step(G)
        number_of_visited_nodes += 1

    return G.nodes[ending_node]["node_weight"]


#################################

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


def greedy_dijkstra(G, starting_node, ending_node):
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

# test()

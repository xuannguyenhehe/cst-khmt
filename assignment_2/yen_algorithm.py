import pandas as pd 

raw_data = pd.read_excel("input.xlsx")
raw_data

import networkx as nx

df = raw_data[["distance", "Source", "Destination"]]
df.Source = df.Source.astype(str)
df.Destination = df.Destination.astype(str)
df.head()

import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
for index, row in df.iterrows():
  source = row["Source"]
  target = row["Destination"]
  distance = row["distance"]
  G.add_edge(source, target, length=distance, weight=distance)

def k_shortest_paths(G, source, target, k=1, weight='weight'):
    if source == target:
        return ([0], [[source]]) 
       
    length, path = nx.single_source_dijkstra(G, source, target, weight=weight)
    if target not in path:
        raise nx.NetworkXNoPath("node %s not reachable from %s" % (source, target))

    if k > G.number_of_edges():
        print("k must <", G.number_of_edges())
  
    lengths = [length]
    paths = [path]
    ls_potential_length = []
    ls_potential_path = []

    for index_solution in range(1, k):
        lastest_path = paths[-1]
        for edge in list(zip(lastest_path[:-1], lastest_path[1:])):
            first_node = edge[0]
            second_node = edge[1]
            temp_G = G.copy()
            temp_G.remove_edge(first_node, second_node)
            try:
                second_length, second_path = nx.single_source_dijkstra(temp_G, first_node, target, weight=weight)
            except:
                continue
            index_first_node = lastest_path.index(first_node)
            first_length = 0
            first_path = lastest_path[:(index_first_node + 1)]

            for u, v in list(zip(first_path[:-1], first_path[1:])):
                edge_attr = temp_G[u][v]
                temp_length = edge_attr["length"]
                first_length += temp_length
            
            temp_length = first_length + second_length
            temp_path = first_path[:-1] + second_path
            if temp_path not in ls_potential_length and temp_path not in paths:
                ls_potential_length.append(temp_length)
                ls_potential_path.append(temp_path)
    
        if len(ls_potential_path):
            while True:
                min_potential_length = min(ls_potential_length)
                index_potential_element = ls_potential_length.index(min_potential_length)
                if ls_potential_path[index_potential_element] not in paths:
                    lengths.append(ls_potential_length[index_potential_element])
                    paths.append(ls_potential_path[index_potential_element])
                    del ls_potential_length[index_potential_element]
                    del ls_potential_path[index_potential_element]
                    break
                else:
                    del ls_potential_length[index_potential_element]
                    del ls_potential_path[index_potential_element]
        
    for index_result, result in enumerate(list(zip(lengths, paths))):
        length, path = result
        # key_G = nx.DiGraph()
        # key_index = 0
        # for first_node, second_node in list(zip(path[:-1], path[1:])):
        #     edge_attr = G[first_node][second_node]
        #     key_G.add_edge(first_node, second_node, length=edge_attr["length"], weight=edge_attr["weight"])
          
        # # nx.draw(key_G, with_labels = True)
        # edge_labels = nx.get_edge_attributes(key_G, 'label')
        # pos = {}
        # for index, row in raw_data.iterrows():
        #     long_value = row["source_long"]
        #     lat_value = row["source_lat"]
        #     source = str(row["Source"])
        #     if source in path:
        #         mx, my = m([float(long_value)], [float(lat_value)])
        #         pos[source] = (mx[0], my[0])
        #     if index == len(raw_data) - 1:
        #         long_value = row["dest_long"]
        #         lat_value = row["dest_lat"]
        #         source = str(row["Destination"])
        #         mx, my = m([float(long_value)], [float(lat_value)])
        #         pos[source] = (mx[0], my[0])
        # plt.figure(figsize = (10, 5))
        # nx.draw_networkx_nodes(
        #     G = key_G, 
        #     pos = pos, 
        #     node_color = 'r', 
        #     alpha = 0.8, 
        #     node_size = 400,
        # )
        # nx.draw_networkx_edges(G = key_G, pos = pos, edge_color='black', alpha=0.2, arrows = True)
        # nx.draw_networkx_labels(key_G, pos, font_size=10)
        # plt.savefig(str(index_result) + '.png')
        # plt.show() 
        print(length, path)
        # print("==============================")
        # break
        

k_shortest_paths(G, '1.0', '15.0', 14, "weight")


pos = {}
for index, row in raw_data.iterrows():
    long_value = row["source_long"]
    lat_value = row["source_lat"]
    source = str(row["Source"])
    mx, my = m(long_value, lat_value)
    pos[source] = (long_value, lat_value)
    if index == len(raw_data) - 1:
        long_value = row["dest_long"]
        lat_value = row["dest_lat"]
        source = str(row["Destination"])
        mx, my = m(float(long_value), float(lat_value))
        pos[source] = (float(long_value), float(lat_value))
plt.figure(figsize = (20, 12))
nx.draw_networkx_nodes(
    G = G, 
    pos = pos, 
    # node_list = G.nodes(), 
    node_color = 'r', 
    alpha = 0.8, 
    node_size = 400,
    # label=True
)
nx.draw_networkx_edges(G = G, pos = pos, edge_color='black', alpha=0.2, arrows = True)
nx.draw_networkx_labels(G, pos, font_size=10)
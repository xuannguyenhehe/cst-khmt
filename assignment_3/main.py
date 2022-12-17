import pandas as pd
import networkx as nx
from louvain.louvain import louvain_communities
from leiden.leiden import leiden_communities
import igraph as ig
from utils.general import get_statistic, get_modularity
import time

def preprocess(path_edges: str, column_name_first: str, column_name_second: str):
    df_edge = pd.read_csv(path_edges)
    df_edge = df_edge[[column_name_first, column_name_second]]
    df_edge = df_edge.dropna()
    # dic = {
    #     'st_id_x': ['A', 'A', 'B', 'B', 'D', 'D'],
    #     'st_id_y': ['B', 'C', 'C', 'D', 'E', 'F'],
    # }
    # df_edge = pd.DataFrame(dic)
    return df_edge

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:  
        type_algorithm = str(sys.argv[3])
        path_edges = str(sys.argv[2])
        path_nodes = str(sys.argv[1]) 
    # type_algorithm = "louvain"
    df_edge = preprocess(path_edges, 'st_id_x', 'st_id_y')    
    internal_time = None

    if type_algorithm == "louvain":
        nx_G = nx.from_pandas_edgelist(df_edge, 'st_id_x', 'st_id_y')
        start_time = time.time()
        list_clusters = louvain_communities(nx_G, seed=21)
        internal_time = time.time() - start_time
    elif type_algorithm == "leiden":
        G = ig.Graph.TupleList(df_edge.itertuples(index=False), weights = False, directed = False)
        nx_G = nx.from_pandas_edgelist(df_edge, 'st_id_x', 'st_id_y')
        start_time = time.time()
        list_clusters = leiden_communities(G)
        internal_time = time.time() - start_time
    else:
        raise ValueError("Could not find type of algorithm you need")

    modularity = get_modularity(nx_G, list_clusters)
    num_cluster = len(list_clusters)
    number_badly_disconnected_communities, ls_num_internal_edges, ls_num_external_edges, relationships \
        = get_statistic(nx_G, list_clusters)
    average_num_internal_edges = sum(ls_num_internal_edges) / len(ls_num_internal_edges)
    average_num_external_edges = sum(ls_num_external_edges) / len(ls_num_external_edges)
    print("=============",type_algorithm,"=============")
    print("run time:", internal_time)
    print("number of cluster:", num_cluster)
    print("modularity:", modularity)
    print("number of badly disconnected communities:", number_badly_disconnected_communities)
    print("average num internal_edges:", average_num_internal_edges)
    print("average num external_edges:", average_num_external_edges)
    print("=============",type_algorithm,"=============")

    df_nodes = pd.read_csv(path_nodes)
    dict_communities = {node: index_community for index_community, community in enumerate(list_clusters) for node in community}
    df_nodes["index_community"] = df_nodes['st_id'].map(dict_communities)
    df_nodes.to_csv("result/" + type_algorithm + ".csv", index=False)

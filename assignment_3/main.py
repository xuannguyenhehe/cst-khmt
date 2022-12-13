import pandas as pd
import networkx as nx
from louvain.louvain import louvain_communities
from leiden.leiden import leiden_communities
import igraph as ig

def preprocess(path_edges: str, column_name_first: str, column_name_second: str, path_nodes: str):
    df_edge = pd.read_csv(path_edges)
    df_edge = df_edge[[column_name_first, column_name_second]]
    df_edge = df_edge.dropna()
    df_node = pd.read_csv(path_nodes)
    dic = {
        'st_id_x': ['A', 'A', 'B', 'B', 'D', 'D'],
        'st_id_y': ['B', 'C', 'C', 'D', 'E', 'F'],
    }
    df_edge = pd.DataFrame(dic)
    return df_edge

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:  # At least 1 command line parameter
        type_algorithm = str(sys.argv[1])

    path_edges = 'dataset/artist_spotify_edge.csv'
    path_nodes = 'dataset/artist_spotify_node.csv'

    df_edge = preprocess(path_edges, 'st_id_x', 'st_id_y', path_nodes)    

    if type_algorithm == "louvain":
        G = nx.from_pandas_edgelist(df_edge, 'st_id_x', 'st_id_y')
        list_clusters = louvain_communities(G, seed=21)
        for i in list_clusters:
            print(len(i), sum([len(j) for j in i]), i) 
    elif type_algorithm == "leiden":
        G = ig.Graph.TupleList(df_edge.itertuples(index=False), weights = False, directed = False)
        list_clusters = leiden_communities(G)
        print(list_clusters)
    else:
        raise ValueError("Could not find type of algorithm you need")

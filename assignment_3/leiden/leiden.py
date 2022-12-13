import time
import pandas as pd
import leidenalg

def leiden_communities(G):
    part = leidenalg.find_partition(G, leidenalg.ModularityVertexPartition)
    max_idx = 0
    print(part.modularity)
    keys = ["id", "cluster"]
    result = [dict(zip(keys, [G.vs["name"][i], part.membership[i] + 1 + max_idx])) for i in range(len(part.membership))]
    df = pd.DataFrame(result)
    return df
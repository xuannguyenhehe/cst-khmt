import time
import pandas as pd
import igraph as ig
t_0 = time.time()
df_topsong = pd.read_csv("/content/edge.csv")
g = ig.Graph.TupleList(df_topsong[["st_id_x", "st_id_y" ]].itertuples(index=False), weights = False, directed = False)
print("TOTAL TIME: ", time.time() - t_0)

import leidenalg
t_0 = time.time()
# part = g.community_leiden()
part = leidenalg.find_partition(g, leidenalg.ModularityVertexPartition)
max_idx = 0
print(part.modularity)
print("TOTAL TIME: ", time.time() - t_0)
keys = ["id", "cluster"]
result = [dict(zip(keys, [g.vs["name"][i], part.membership[i] + 1 + max_idx])) for i in range(len(part.membership))]
df = pd.DataFrame(result)
print(df)
import leidenalg

def leiden_communities(G):
    part = leidenalg.find_partition(G, leidenalg.ModularityVertexPartition)
    number_communities = len(part)

    result = [set() for _ in range(number_communities)] 
    [result[part.membership[i]].update({G.vs["name"][i]}) for i in range(len(part.membership))]
    return result
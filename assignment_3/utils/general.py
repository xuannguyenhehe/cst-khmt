import copy

def get_statistic(G, communities):
    ls_communities = copy.deepcopy(communities)
    number_badly_disconnected_communities = 0
    ls_num_internal_edges = [0 for _ in range(len(ls_communities))]
    ls_num_external_edges = [0 for _ in range(len(ls_communities))]
    for u, v in G.edges:
        for index_community, community in enumerate(communities):
            if u in community and v in community:
                ls_communities[index_community] .difference_update({u, v})
                ls_num_internal_edges[index_community] += 1
                # break
            elif u in community or v in community:
                ls_num_external_edges[index_community] += 1

    for index, checked_community in enumerate(ls_communities):
        if len(checked_community) > 0 and len(communities[index]) > 1:
            number_badly_disconnected_communities += 1
    return number_badly_disconnected_communities, ls_num_internal_edges, ls_num_external_edges

def get_modularity(G, communities, weight="weight", resolution=1):
    if not isinstance(communities, list):
        communities = list(communities)

    directed = G.is_directed()
    if directed:
        out_degree = dict(G.out_degree(weight=weight))
        in_degree = dict(G.in_degree(weight=weight))
        m = sum(out_degree.values())
        norm = 1 / m**2
    else:
        out_degree = in_degree = dict(G.degree(weight=weight))
        deg_sum = sum(out_degree.values())
        m = deg_sum / 2
        norm = 1 / deg_sum**2

    def community_contribution(community):
        comm = set(community)
        L_c = sum(wt for u, v, wt in G.edges(comm, data=weight, default=1) if v in comm)

        out_degree_sum = sum(out_degree[u] for u in comm)
        in_degree_sum = sum(in_degree[u] for u in comm) if directed else out_degree_sum

        return L_c / m - resolution * out_degree_sum * in_degree_sum * norm

    return sum(map(community_contribution, communities))

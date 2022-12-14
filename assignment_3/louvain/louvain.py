from collections import defaultdict, deque
import networkx as nx
from networkx.utils import py_random_state

@py_random_state("seed")
def louvain_communities(
    G, weight="weight", resolution=1, threshold=0.0000001, seed=None
):
    d = louvain_partitions(G, weight, resolution, threshold, seed)
    q = deque(d, maxlen=1)
    return q.pop()

def modularity(G, communities, weight="weight", resolution=1):
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

@py_random_state("seed")
def louvain_partitions(
    G, weight="weight", resolution=1, threshold=0.0000001, seed=None
):
    partition = [{u} for u in G.nodes()]
    mod = modularity(G, partition, resolution=resolution, weight=weight)
    is_directed = G.is_directed()

    graph = G.__class__()
    graph.add_nodes_from(G)
    graph.add_weighted_edges_from(G.edges(data=weight, default=1))

    m = graph.size(weight="weight")
    partition, inner_partition, improvement = _one_level(
        graph, m, partition, resolution, is_directed, seed
    )
    improvement = True
    while improvement:
        yield [s.copy() for s in partition]
        new_mod = modularity(
            graph, inner_partition, resolution=resolution, weight="weight"
        )
        if new_mod - mod <= threshold:
            return
        mod = new_mod
        graph = _gen_graph(graph, inner_partition)
        partition, inner_partition, improvement = _one_level(
            graph, m, partition, resolution, is_directed, seed
        )

def _one_level(G, m, partition, resolution=1, is_directed=False, seed=None):
    node2com = {u: i for i, u in enumerate(G.nodes())}
    inner_partition = [{u} for u in G.nodes()]

    degrees = dict(G.degree(weight="weight"))
    Stot = [deg for deg in degrees.values()]
    nbrs = {u: {v: data["weight"] for v, data in G[u].items() if v != u} for u in G}

    rand_nodes = list(G.nodes)
    seed.shuffle(rand_nodes)
    nb_moves = 1
    improvement = False
    while nb_moves > 0:
        nb_moves = 0
        for u in rand_nodes:
            best_mod = 0
            best_com = node2com[u]
            weights2com = _neighbor_weights(nbrs[u], node2com)

            degree = degrees[u]
            Stot[best_com] -= degree
            remove_cost = -weights2com[best_com] / m + resolution * (
                Stot[best_com] * degree
            ) / (2 * m**2)

            for nbr_com, wt in weights2com.items():
                gain = (
                    remove_cost
                    + wt / m
                    - resolution * (Stot[nbr_com] * degree) / (2 * m**2)
                )
                if gain > best_mod:
                    best_mod = gain
                    best_com = nbr_com

            Stot[best_com] += degree

            if best_com != node2com[u]:
                com = G.nodes[u].get("nodes", {u})
                partition[node2com[u]].difference_update(com)
                inner_partition[node2com[u]].remove(u)
                partition[best_com].update(com)
                inner_partition[best_com].add(u)
                improvement = True
                nb_moves += 1
                node2com[u] = best_com
    partition = list(filter(len, partition))
    inner_partition = list(filter(len, inner_partition))
    return partition, inner_partition, improvement


def _neighbor_weights(nbrs, node2com):
    weights = defaultdict(float)
    for nbr, wt in nbrs.items():
        weights[node2com[nbr]] += wt
    return weights


def _gen_graph(G, partition):
    H = G.__class__()
    node2com = {}
    for i, part in enumerate(partition):
        nodes = set()
        for node in part:
            node2com[node] = i
            nodes.update(G.nodes[node].get("nodes", {node}))
        H.add_node(i, nodes=nodes)

    for node1, node2, wt in G.edges(data=True):
        wt = wt["weight"]
        com1 = node2com[node1]
        com2 = node2com[node2]
        temp = H.get_edge_data(com1, com2, {"weight": 0})["weight"]
        H.add_edge(com1, com2, **{"weight": wt + temp})
    return H
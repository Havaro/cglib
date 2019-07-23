from cg.game import Game
from itertools import permutations
from tqdm import tqdm
import networkx as nx


def read_canonical_forms(path):
    with open(path) as f:
        return [line.strip() for line in f]


def create_network(canons):
    # Create network
    net = nx.DiGraph()

    # Check all (G, H) pairs
    num_perms = int(len(canons) * (len(canons) - 1))
    perms = permutations(canons, 2)
    for G, H in tqdm(perms, total=num_perms):
        # Check whether G > H
        if Game(G).gtr(Game(H)):
            net.add_edge(G, H)

    # Return the transitive reduction
    red = nx.algorithms.dag.transitive_reduction(net)
    return red.edges


def save_edgelist(edges, path):
    with open(path, "w") as f:
        f.write("source;target\n")
        for G, H in edges:
            f.write(f"{G};{H}\n")


canon_list = read_canonical_forms("groups_research/results/g03.txt")
edges = create_network(canon_list)
save_edgelist(edges, "groups_research/resuls/adj_list_g03.csv")

import networkx as nx
import matplotlib.pyplot as plt

def filetograph(filename):
    G = nx.Graph()
    with open(filename) as f:
        f = f.readlines()
        for line in f[1:]:
            line = line.strip()
            match line.split():
                case [node1, node2]:
                    G.add_edge(int(node1), int(node2))
                case [node1, node2, *a]:
                    G.add_edge(int(node1), int(node2))
                case _:
                    print(f"Skipping invalid line: {line}")

    pos = nx.spring_layout(G)

    return G


files = ["net1.txt", "net2.txt", "net3.txt", "huge.txt", "big.txt"]

for file in files:
    nx.write_gexf(filetograph(file),  file[:-4] + ".gexf")
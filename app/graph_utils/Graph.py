import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, root, leaf):
        self.root = root
        self.leaf = leaf
        self.networkx = nx.DiGraph()

    def getPath(self):
        self.path = nx.shortest_path(self.networkx, self.root, self.leaf)

    def draw(self):
        plt.tight_layout()
        nx.draw_networkx(self.networkx, arrows=True)
        plt.savefig("/Users/s163799/Documents/g1.png", format="PNG")
        plt.clf()

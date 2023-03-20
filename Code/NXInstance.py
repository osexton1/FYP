import networkx as nx
import matplotlib.pyplot as plt

class NXInstance:

    def __init__(self, sourcefile):
        self.__graph = nx.read_gml(sourcefile)
        nx.draw_circular(self.__graph, with_labels=True)
        plt.savefig('sourceGraph.png')
        plt.clf()

    def getGraph(self):
        return self.__graph

    def getEdges(self):
        return self.__graph.edges.data()

    def getVertices(self):
        return self.__graph.nodes.data()

    def search(self, a, b):
        return nx.dijkstra_path(self.__graph, a, b)

    def removeEdge(self, a, b):
        self.__graph.remove_edge(a, b)

    def addEdge(self, a, b):
        self.__graph.add_edge(a, b)

    def drawGraph(self):
        nx.write_graphml(self.__graph, "./outputGraph")
        nx.draw_circular(self.__graph, with_labels=True)
        plt.savefig('outputGraph.png')


if __name__ == "__main__":
    testGraph = NXInstance("graph.txt")
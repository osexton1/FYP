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

    def minEdgeCut(self, a, b):
        return nx.minimum_edge_cut(self.__graph, a, b)

    def drawGraph(self, fileName):
        nx.write_graphml(self.__graph, "./outputGraphs/%s" % fileName)
        nx.draw_circular(self.__graph, with_labels=True)
        plt.savefig('./outputGraphs/%s.png' % fileName)


if __name__ == "__main__":
    testGraph = NXInstance("graph.txt")
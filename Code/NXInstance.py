import networkx as nx

class NXInstance:

    def __init__(self, sourcefile):
        self.__graph = nx.read_gml(sourcefile)

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

if __name__ == "__main__":
    testGraph = NXInstance("graph.txt")
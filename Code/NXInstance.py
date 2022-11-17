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

if __name__ == "__main__":
    testGraph = NXInstance("graph.txt")
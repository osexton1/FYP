from NXInstance import *

class Searcher:

    def __init__(self, nx_graph):
        self.__graph = nx_graph
        self.__vertices = nx_graph.getVertices()
        self.__edges = {}
        edges = nx_graph.getEdges()
        for edge in edges:
            self.__edges[(edge[0], edge[1])] = bool(edge[2]["included"])

    def getGraph(self):
        return self.__graph

    def searchGraph(self, a, b):
        return self.__graph.search(a, b)

    def removeEdge(self, a, b):
        self.__graph.removeEdge(a, b)

if __name__ == "__main__":
    graph = NXInstance("graph.txt")
    searcher = Searcher(graph)
    print()
    print(searcher.searchGraph('Node 1', 'Node 10'))
    print()
    searcher.removeEdge('Node 1', 'Node 2')
    print()
    print(searcher.getGraph().getEdges())
    print()
    print(searcher.searchGraph('Node 1', 'Node 10'))
    print()

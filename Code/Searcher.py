from NXInstance import *

class Searcher:

    def __init__(self, nx_graph):
        self.__vertices = nx_graph.getVertices()
        self.__edges = {}
        edges = nx_graph.getEdges()
        for edge in edges:
            self.__edges[(edge[0], edge[1])] = bool(edge[2]["included"])
        print(self.__edges)

if __name__ == "__main__":
    graph = NXInstance("graph.txt")
    searcher = Searcher(graph)
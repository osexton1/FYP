from NXInstance import *

class Searcher:

    def __init__(self, nx_graph):
        self.__graph = nx_graph
        self.__vertices = self.__graph.getVertices()
        self.__pathsLegal = []
        self.__pathsIllegal = []
        paths = open('paths.txt', 'r')
        for path in paths:
            path = path.strip('\n')
            path = path.split(', ')
            if path[0] == 'Legal':
                self.__pathsLegal.append((path[1], path[2]))
            else:
                self.__pathsIllegal.append((path[1], path[2]))
        paths.close()
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

    def computeGraph(self):
        invalidTraversable = True
        while invalidTraversable:
            validPaths = []
            illegalPaths = []
            try:
                for path in self.__pathsLegal:
                    validPaths.append(self.searchGraph(path[0], path[1]))
            except nx.exception.NetworkXNoPath:
                print('It is not possible to compute such a graph')
            try:
                for path in self.__pathsIllegal:
                    illegalPaths.append(self.searchGraph(path[0], path[1]))
            except nx.exception.NetworkXNoPath:
                if len(self.__pathsIllegal) > 1:
                    self.__pathsIllegal = self.__pathsIllegal[1:]
                    continue
                else:
                    self.__pathsIllegal = []
                    continue
            
            if len(self.__pathsIllegal) > 0:
                last_node = illegalPaths[0].pop()
                second_last_node = illegalPaths[0].pop()
                self.removeEdge(second_last_node, last_node)
                print('Removed Edge: ' + second_last_node + ' -> ' + last_node)
            else:
                print('It is possible to compute a graph where no illegal paths are traversable')
                invalidTraversable = False

    def drawGraph(self):
        self.__graph.drawGraph()

if __name__ == "__main__":
    graph = NXInstance("graph.txt")
    searcher = Searcher(graph)
    searcher.computeGraph()
    searcher.drawGraph()

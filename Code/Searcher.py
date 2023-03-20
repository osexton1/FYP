from NXInstance import *
from random import randint
from time import time

class Searcher:

    def __init__(self, nx_graph, graph_file):
        self.__graph = nx_graph
        self.__original_state = graph_file
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

    def addEdge(self, a, b):
        self.__graph.addEdge(a, b)

    def computeGraphV1(self):
        # All paths will always be traversable at the first loop
        invalidTraversable = True
        while invalidTraversable:
            validPaths = []
            illegalPaths = []
            try:
                for path in self.__pathsLegal:
                    validPaths.append(self.searchGraph(path[0], path[1]))
            except nx.exception.NetworkXNoPath:
                """
                    All paths are traversable at the first check, so this code 
                    should only be reached at the second pass.

                    If valid paths are broken, remove the next edge in the illegal
                    path and then restore the original moved edge
                """
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
            # Modify this to store the removed edge in case it breaks valid paths
            if len(self.__pathsIllegal) > 0:
                last_node = illegalPaths[0].pop()
                second_last_node = illegalPaths[0].pop()
                self.removeEdge(second_last_node, last_node)
                print('Removed Edge: ' + second_last_node + ' -> ' + last_node)
            else:
                print('It is possible to compute a graph where no illegal paths are traversable')
                invalidTraversable = False

    def computeGraphV2(self):
        # All paths will always be traversable at the first loop
        removedEdges = []
        validPaths = []
        illegalPaths = []
        legalBroken = False
        invalidTraversable = True
        while invalidTraversable:
            try:
                for path in self.__pathsLegal:
                    if self.searchGraph(path[0], path[1]) not in validPaths:
                        validPaths.append(self.searchGraph(path[0], path[1]))
            except nx.exception.NetworkXNoPath:
                legalBroken = True
                continue
            try:
                for path in self.__pathsIllegal:
                    if self.searchGraph(path[0], path[1]) not in illegalPaths:
                        illegalPaths.append(self.searchGraph(path[0], path[1]))
            except nx.exception.NetworkXNoPath:
                continue
            # Modify this to store the removed edge in case it breaks valid paths
            for path in illegalPaths:
                print('Path: ' + str(path))
                last_node = illegalPaths[0].pop()
                second_last_node = illegalPaths[0].pop()
                self.removeEdge(second_last_node, last_node)
                removedEdges.append((second_last_node, last_node))
                print('Removed Edge: ' + second_last_node + ' -> ' + last_node)

            if legalBroken and len(removedEdges) > 0:
                u, v = removedEdges.pop(0)
                self.addEdge(u, v)
                print('Restored Edge: ' + u + ' -> ' + v)
                print('Illegal Paths after Restoration: ' + str(illegalPaths))
                print(removedEdges)
                legalBroken = False
            elif legalBroken and not len(removedEdges) > 0:
                print('Here')
                continue
            else:
                print('It is not possible to compute such a graph')
                invalidTraversable = False
            # else:
            #     print('It is possible to compute a graph where no illegal paths are traversable')
            #     invalidTraversable = False

    def computeCutsV1(self, timeout):
        legal = [path for path in self.__pathsLegal]
        illegal = [path for path in self.__pathsIllegal]
        start_time = time()
        removedEdges = []
        time_remains = True
        while time_remains:
            for pair in illegal:
                try:
                    print('Testing Illegal Path: ' + str(pair))
                    path = self.searchGraph(pair[0], pair[1])
                    print('Found Illegal Path: ' + str(path))
                    print()
                    max_index = len(path) - 1
                    remove_index = randint(0, max_index)
                    if remove_index == max_index:
                        self.removeEdge(path[remove_index-1], path[remove_index])
                        removedEdges.append((path[remove_index-1], path[remove_index]))
                    else:
                        self.removeEdge(path[remove_index], path[remove_index+1])
                        removedEdges.append((path[remove_index], path[remove_index+1]))
                except:
                    # Should only reach this case if the path is already not traversable
                    if len(illegal):
                        illegal.pop(0)
                    else:
                        time_remains = False
                        print("The graph is already appropriately configured")
                        return self.drawGraph()
            for pair in legal:
                try:
                    print('Testing Legal Path: ' + str(pair))
                    path = self.searchGraph(pair[0], pair[1])
                    print('Found Legal Path: ' + str(path))
                    print()
                except:
                    # A legal path is broken -> reset and start over
                    print('Failed to find Legal Path')
                    print('=== RESETTING ===')
                    self.__graph = NXInstance(self.__original_state)
                    removedEdges = []
                    illegal = [path for path in self.__pathsIllegal]
                    legal = [path for path in self.__pathsLegal]
                    break
            # Don't want to use nx exception for loop control
            illegalCounter = 0
            for pair in illegal:
                try:
                    print('Testing Illegal Path: %s again' % str(pair))
                    path = self.searchGraph(pair[0], pair[1])
                    print('Found Illegal Path: %s again' % str(path))
                    print()
                    illegalCounter += 1
                    time_passed = time() - start_time
                    if time_passed < timeout:
                        break
                    elif time_passed > timeout:
                        time_remains = False
                        print("Timed Out Illegal")
                        break
                except:
                    break
            legalCounter = len(legal)
            for pair in legal:
                try:
                    print('Testing Legal Path: %s again' % str(pair))
                    path = self.searchGraph(pair[0], pair[1])
                    print('Found Legal Path: %s again' % str(path))
                    print()
                    legalCounter -= 1
                    time_passed = time() - start_time
                    if time_passed < timeout:
                        break
                    elif time_passed > timeout:
                        time_remains = False
                        print("Timed Out Legal")
                        break
                except:
                    break
            if illegalCounter == 0 and legalCounter == 0:
                time_remains = False
                print("Success!!")
                print("Removed: " + str(removedEdges))
                self.drawGraph()

    def drawGraph(self):
        self.__graph.drawGraph()

if __name__ == "__main__":
    graph = NXInstance("graph.txt")
    searcher = Searcher(graph, "graph.txt")
    searcher.computeGraphV1()
    searcher.drawGraph()

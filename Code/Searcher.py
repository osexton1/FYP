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

    def minEdgeCut(self, a, b):
        return self.__graph.minEdgeCut(a, b)

    def computeGraphV1(self):
        invalidTraversable = True
        validPaths = []
        for path in self.__pathsLegal:
            try:
                self.searchGraph(path[0], path[1])
            except nx.exception.NetworkXNoPath:
                """
                    If an error occurs here, it is never possible to connect a pair
                    of nodes in a legal path
                """
                print('It is not possible to compute such a graph')
                invalidTraversable = False

        while invalidTraversable:
            illegalPaths = []
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
            else:
                legalCounter = len(validPaths)
                for path in self.__pathsLegal:
                    try:
                        self.searchGraph(path[0], path[1])
                        legalCounter -= 1
                    except:
                        print('It is not possible to compute such a graph')
                        invalidTraversable = False
                        break
                if legalCounter == 0:
                    print('It is possible to compute a graph where no illegal paths are traversable')
                    invalidTraversable = False
                    self.drawGraph('outputGraphV1')

    def computeGraphV2(self):
        validPaths = []
        invalidTraversable = True
        for path in self.__pathsLegal:
            try:
                self.searchGraph(path[0], path[1])
            except nx.exception.NetworkXNoPath:
                """
                    If an error occurs here, it is never possible to connect a pair
                    of nodes in a legal path
                """
                print('It is not possible to compute such a graph')
                invalidTraversable = False
        while invalidTraversable:
            illegalPaths = []
            try:
                for path in self.__pathsLegal:
                    if self.searchGraph(path[0], path[1]) not in validPaths:
                        validPaths.append(self.searchGraph(path[0], path[1]))
            except nx.exception.NetworkXNoPath:
                continue
            try:
                for path in self.__pathsIllegal:
                    if self.searchGraph(path[0], path[1]) not in illegalPaths:
                        illegalPaths.append(self.searchGraph(path[0], path[1]))
            except nx.exception.NetworkXNoPath:
                continue

            for path in illegalPaths:
                last_node = path.pop()
                next_node = path.pop()
                pair = (next_node, last_node)
                self.removeEdge(next_node, last_node)
                for validPath in self.__pathsLegal:
                    try:     
                        self.searchGraph(validPath[0], validPath[1])
                    except nx.exception.NetworkXNoPath:
                        validBroken = True
                        while validBroken:
                            # Remove next edge from sequence
                            next_removed = path.pop()
                            self.removeEdge(next_removed, pair[0])
                            # Restore the original removed edge
                            self.addEdge(pair[0], pair[1])
                            pair = (next_removed, pair[0])
                            try:     
                                route = self.searchGraph(validPath[0], validPath[1])
                                validBroken = False
                            except nx.exception.NetworkXNoPath:
                                print('It is not possible to compute such a graph')
                                invalidTraversable, validBroken = False
                                break    
            illegalCounter = 0
            for pair in self.__pathsIllegal:
                try:
                    path = self.searchGraph(pair[0], pair[1])
                    illegalCounter += 1
                except:
                    continue
            if illegalCounter == 0:
              print("It is possible to compute a graph where no illegal paths are traversable")
              invalidTraversable = False
              self.drawGraph('outputGraphV2')
            
    def computeCutsV1(self, timeout):
        legal = [path for path in self.__pathsLegal]
        illegal = [path for path in self.__pathsIllegal]
        start_time = time()
        removedEdges = []
        time_remains = True
        for path in self.__pathsLegal:
            try:
                self.searchGraph(path[0], path[1])
            except nx.exception.NetworkXNoPath:
                """
                    If an error occurs here, it is never possible to connect a pair
                    of nodes in a legal path
                """
                print('It is not possible to compute such a graph')
                time_remains = False
        while time_remains:
            for pair in illegal:
                try:
                    print('Testing Illegal Path: ' + str(pair))
                    path = self.searchGraph(pair[0], pair[1])
                    print('Found Illegal Path: ' + str(path))
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
                    continue
            for pair in legal:
                try:
                    print('Testing Legal Path: ' + str(pair))
                    path = self.searchGraph(pair[0], pair[1])
                    print('Found Legal Path: ' + str(path))
                except:
                    # A legal path is broken -> reset and start over
                    print('Failed to find Legal Path')
                    print('=== RESETTING ===')
                    self.__graph = NXInstance(self.__original_state)
                    removedEdges = []
                    illegal = [path for path in self.__pathsIllegal]
                    legal = [path for path in self.__pathsLegal]
                    break
            illegalCounter = 0
            for pair in illegal:
                try:
                    print('Testing Illegal Path: %s again' % str(pair))
                    path = self.searchGraph(pair[0], pair[1])
                    print('Found Illegal Path: %s again' % str(path))
                    illegalCounter += 1
                    time_passed = time() - start_time
                    if time_passed < timeout:
                        continue
                    elif time_passed > timeout:
                        time_remains = False
                        break
                except:
                    continue
            legalCounter = len(legal)
            for pair in legal:
                try:
                    print('Testing Legal Path: %s again' % str(pair))
                    path = self.searchGraph(pair[0], pair[1])
                    print('Found Legal Path: %s again' % str(path))
                    legalCounter -= 1
                    time_passed = time() - start_time
                    if time_passed < timeout:
                        continue
                    elif time_passed > timeout:
                        time_remains = False
                        print()
                        print("Timed Out")
                        print()
                        break
                except:
                    break
            if illegalCounter == 0 and legalCounter == 0:
                time_remains = False
                print("Success!!")
                print("Removed: " + str(removedEdges))
                self.drawGraph('outputGraphCutsV1')

    def computeCutsV2(self, timeout):
        legal = [path for path in self.__pathsLegal]
        illegal = [path for path in self.__pathsIllegal]
        start_time = time()
        doNotRemove = []
        removedEdges = []
        time_remains = True
        for path in self.__pathsLegal:
            try:
                self.searchGraph(path[0], path[1])
            except nx.exception.NetworkXNoPath:
                """
                    If an error occurs here, it is never possible to connect a pair
                    of nodes in a legal path
                """
                print('It is not possible to compute such a graph')
                time_remains = False
        for pair in legal:
            for edge in self.minEdgeCut(pair[0], pair[1]):
                if edge not in doNotRemove:
                    doNotRemove.append(edge)
        while time_remains:
            for pair in illegal:
                try:
                    print('Testing Illegal Path: ' + str(pair))
                    path = self.searchGraph(pair[0], pair[1])
                    print('Found Illegal Path: ' + str(path))
                    max_index = len(path) - 1
                    remove_index = randint(0, max_index)
                    if remove_index == max_index:
                        if (path[remove_index-1], path[remove_index]) not in doNotRemove: 
                            self.removeEdge(path[remove_index-1], path[remove_index])
                            removedEdges.append((path[remove_index-1], path[remove_index]))
                    else:
                        if (path[remove_index], path[remove_index+1]) not in doNotRemove:
                            self.removeEdge(path[remove_index], path[remove_index+1])
                            removedEdges.append((path[remove_index], path[remove_index+1]))
                except:
                    # Should only reach this case if the path is already not traversable
                    continue
            for pair in legal:
                try:
                    print('Testing Legal Path: ' + str(pair))
                    path = self.searchGraph(pair[0], pair[1])
                    print('Found Legal Path: ' + str(path))
                except:
                    # A legal path is broken -> reset and start over
                    print('Failed to find Legal Path')
                    print('=== RESETTING ===')
                    self.__graph = NXInstance(self.__original_state)
                    removedEdges = []
                    illegal = [path for path in self.__pathsIllegal]
                    legal = [path for path in self.__pathsLegal]
                    break
            illegalCounter = 0
            for pair in illegal:
                try:
                    print('Testing Illegal Path: %s again' % str(pair))
                    path = self.searchGraph(pair[0], pair[1])
                    print('Found Illegal Path: %s again' % str(path))
                    illegalCounter += 1
                    time_passed = time() - start_time
                    if time_passed < timeout:
                        continue
                    elif time_passed > timeout:
                        time_remains = False
                        break
                except:
                    continue
            legalCounter = len(legal)
            for pair in legal:
                try:
                    print('Testing Legal Path: %s again' % str(pair))
                    path = self.searchGraph(pair[0], pair[1])
                    print('Found Legal Path: %s again' % str(path))
                    legalCounter -= 1
                    time_passed = time() - start_time
                    if time_passed < timeout:
                        continue
                    elif time_passed > timeout:
                        time_remains = False
                        print()
                        print("Timed Out")
                        print()
                        break
                except:
                    break
            if illegalCounter == 0 and legalCounter == 0:
                time_remains = False
                print("Success!!")
                print("Removed %d edges" % len(removedEdges))
                print("Removed: " + str(removedEdges))
                self.drawGraph('outputGraphCutsV2')

    def drawGraph(self, fileName):
        self.__graph.drawGraph(fileName)

if __name__ == "__main__":
    graph = NXInstance("graph.txt")
    searcher = Searcher(graph, "graph.txt")
    # searcher.computeGraphV1()
    # searcher.computeGraphV2()
    # searcher.computeCutsV1(120)
    searcher.computeCutsV2(120)

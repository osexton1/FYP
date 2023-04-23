from Searcher import *
from NXInstance import *
from graphBuilder import *

import time

def my_function(searcher):
    searching = searcher
    searching.computeGraphV1()
    # searching.computeGraphV2()
    # searching.computeCutsV1(300)
    # searching.computeCutsV2(300)


run_times = []
# Runs each algorithm 50 times to get the mean run time
for i in range(50):
    # Builds a randomly generated graph of x nodes and y edges
    graphBuilder(100, 4500)
    graph = NXInstance("graphExp.txt")
    searcher = Searcher(graph, "graphExp.txt")
    start = time.time()
    my_function(searcher)
    end = time.time()
    run_times.append(end - start)

mean_run_time = sum(run_times) / len(run_times)
print("Mean run time: %.2f seconds" % mean_run_time)
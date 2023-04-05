import random

num_nodes = 25
num_edges = 50
existing_edges = set()

graph = open('graph50.txt', 'w')

graph.write(f"graph [\n\tcomment \"This is a graph of {num_nodes} nodes\"\n\tdirected 1\n\tIsPlanar 1\n")

for i in range(1, num_nodes+1):
    graph.write(f"\tnode [\n\t\tid {i}\n\t\tlabel\n\t\t\"Node {i}\"\n\t]\n")

for i in range(num_edges):
    source = random.randint(1, num_nodes)
    target = random.randint(1, num_nodes)
    while source == target or (source, target) in existing_edges:
        target = random.randint(1, num_nodes)
    weight = random.randint(1, 20)
    included = 1
    graph.write(f"\tedge [\n\t\tsource {source}\n\t\ttarget {target}\n\t\tweight {weight}\n\t\tincluded {included}\n\t]\n")
    graph.write(f"\tedge [\n\t\tsource {target}\n\t\ttarget {source}\n\t\tweight {weight}\n\t\tincluded {included}\n\t]\n")
    existing_edges.add((source, target))
    existing_edges.add((target, source))

graph.write("]")

graph.close()

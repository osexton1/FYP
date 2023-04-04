import random

num_nodes = 50
num_edges = 150
existing_edges = set()

graph = open('graph50.txt', 'w')

graph.write(f"graph [\n\tcomment \"This is a graph of 50 nodes\"\n\tdirected 1\n\tIsPlanar 1\n")

for i in range(1, 51):
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


num_pairs = 20
existing_pairs = set()

paths = open('paths50.txt', 'w')

for i in range(num_pairs):
    node1 = random.randint(1, num_nodes)
    node2 = random.randint(1, num_nodes)
    while node1 == node2 or (node1, node2) in existing_edges:
        node2 = random.randint(1, num_nodes)
    legal = random.choice([True, False])
    if legal:
        paths.write(f"Legal, Node {node1}, Node {node2}\n")
    else:
        paths.write(f"Illegal, Node {node1}, Node {node2}\n")
    existing_pairs.add((node1, node2))
import random

def graphBuilder(num_nodes, num_edges):
    num_nodes = num_nodes
    num_edges = num_edges
    existing_edges = set()

    graph = open('graphExp.txt', 'w')

    graph.write(f"graph [\n\tcomment \"This is a graph of {num_nodes} nodes\"\n\tdirected 1\n\tIsPlanar 1\n")

    for i in range(1, num_nodes+1):
        graph.write(f"\tnode [\n\t\tid {i}\n\t\tlabel\n\t\t\"Node {i}\"\n\t]\n")

    for i in range(num_edges//2):
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

    paths = open('paths.txt', 'w')

    max_restrictions = (num_nodes*4)//10
    paths_assigned = []
    for i in range(max_restrictions):
        if i < max_restrictions//2:
            source = random.randint(1, num_nodes)
            target = random.randint(1, num_nodes)
            while source == target or (source, target) in paths_assigned:
                target = random.randint(1, num_nodes)
            paths.write(f"Legal, Node {source}, Node {target}\n")
            paths_assigned.append((source, target))
        else:
            source = random.randint(1, num_nodes)
            target = random.randint(1, num_nodes)
            while source == target or (source, target) in paths_assigned:
                target = random.randint(1, num_nodes)
            paths.write(f"Illegal, Node {source}, Node {target}\n")
            paths_assigned.append((source, target))

    paths.close()

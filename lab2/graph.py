from collections import deque
import copy
import random
import matplotlib.pyplot as plot


# Undirected graph using an adjacency list


class Graph:

    def __init__(self, n):
        self.adj = {}
        for i in range(n):
            self.adj[i] = []

    def are_connected(self, node1, node2):
        return node2 in self.adj[node1]

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self):
        self.adj[len(self.adj)] = []

    def add_edge(self, node1, node2):
        if node1 not in self.adj[node2]:
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)

    def number_of_nodes(self):
        return len(self.adj)

    def get_size(self):
        return len(self.adj)


# Breadth First Search
def BFS(G, node1, node2):
    Q = deque([node1])
    marked = {node1: True}
    for node in G.adj:
        if node != node1:
            marked[node] = False
    while len(Q) != 0:
        current_node = Q.popleft()
        for node in G.adj[current_node]:
            if node == node2:
                return True
            if not marked[node]:
                Q.append(node)
                marked[node] = True
    return False


# Depth First Search
def DFS(G, node1, node2):
    S = [node1]
    marked = {}
    for node in G.adj:
        marked[node] = False
    while len(S) != 0:
        current_node = S.pop()
        if not marked[current_node]:
            marked[current_node] = True
            for node in G.adj[current_node]:
                if node == node2:
                    return True
                S.append(node)
    return False


# Use the methods below to determine minimum Vertex Covers
def add_to_each(sets, element):
    copy = sets.copy()
    for set in copy:
        set.append(element)
    return copy


def power_set(set):
    if set == []:
        return [[]]
    return power_set(set[1:]) + add_to_each(power_set(set[1:]), set[0])


def is_vertex_cover(G, C):
    for start in G.adj:
        for end in G.adj[start]:
            if not (start in C or end in C):
                return False
    return True


def MVC(G):
    nodes = [i for i in range(G.get_size())]
    subsets = power_set(nodes)
    min_cover = nodes
    for subset in subsets:
        if is_vertex_cover(G, subset):
            if len(subset) < len(min_cover):
                min_cover = subset
    return min_cover

# BFS2 and DFS2 Implementation


def BFS2(G, node1, node2):
    visited = set()
    queue = deque([(node1, [node1])])

    while queue:
        current_node, path = queue.popleft()
        visited.add(current_node)

        if current_node == node2:
            return path

        for neighbor in G.adjacent_nodes(current_node):
            if neighbor not in visited:
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))

    return []


def DFS2(G, node1, node2, visited=None):
    if visited is None:
        visited = set()

    visited.add(node1)

    if node1 == node2:
        return [node1]

    for neighbor in G.adjacent_nodes(node1):
        if neighbor not in visited:
            path = DFS2(G, neighbor, node2, visited)
            if path:
                return [node1] + path

    return []

# BFS3 Predecessor Dictionary


def BFS3(G, node1):
    queue = deque([node1])
    predDictionary = {}
    marked = {node1: True}
    for node in G.adj:
        if node != node1:
            marked[node] = False

    while len(queue) != 0:
        currentNode = queue.popleft()

        for adjacentNode in G.adj[currentNode]:
            if marked[adjacentNode] == False:
                queue.append(adjacentNode)
                marked[adjacentNode] = True
                predDictionary[adjacentNode] = currentNode

    return predDictionary


# DFS3 Predecessor Dictionary
def DFS3(G, node1, marked=None, predDictionary=None):
    currentNode = node1

    if not marked:
        marked = {currentNode: True}
        for node in G.adj:
            if node != currentNode:
                marked[node] = False

    if not predDictionary:
        predDictionary = {}

    # explore adjacent nodes
    for adjacentNode in G.adj[currentNode]:
        if marked[adjacentNode] == False:
            marked[adjacentNode] = True
            predDictionary[adjacentNode] = currentNode
            # pass the updated marked dictionary and updated predDictionary
            DFS3(G, adjacentNode, marked, predDictionary)

    return predDictionary


def has_cycle(G):
    visited = set()

    def inner_cycle_detection(current, prev):
        visited.add(current)
        for neighbor in G.adj[current]:
            if neighbor not in visited:
                if inner_cycle_detection(neighbor, current):
                    return True
            elif neighbor != prev:
                return True
        return False
    for node in G.adj:
        if node not in visited:
            if inner_cycle_detection(node, -1):
                return True
    return False


def is_connected(G):
    start_node = list(G.adj.keys())[0]
    gone_to = set()
    queue = deque([start_node])
    while queue:
        node = queue.popleft()
        gone_to.add(node)
        for neighbor in G.adj[node]:
            if neighbor not in gone_to:
                queue.append(neighbor)
    return len(gone_to) == len(G.adj)


def create_random_graph(i, j):
    random_graph = Graph(i)

    max_edges = int((i * (i - 1)) / 2)  # Maximum number of edges in a graph

    j = min(j, max_edges)  # Ensure j is < max_edges

    # random edge generation
    edges_added = 0
    while edges_added < j:
        node1 = random.randint(0, i - 1)
        node2 = random.randint(0, i - 1)

        # ensure node1 and node2 are not the same node and that the edge does not already exist
        if node1 != node2 and not random_graph.are_connected(node1, node2):
            random_graph.add_edge(node1, node2)
            edges_added += 1

    return random_graph


# exp1 code
def calc_cy_p(x, n, m, step):
    cycle_probabilities = []
    edge_counts = list(range(0, n+1, step))

    for j in edge_counts:
        cycle_count = 0
        for i in range(m):
            G = create_random_graph(x, j)
            if has_cycle(G):
                cycle_count += 1

        cycle_probabilities.append(cycle_count / m)
    return edge_counts, cycle_probabilities


def plot_cy_p(x, n, m, step):
    edge_counts, cycle_probabilities = calc_cy_p(x, n, m, step)

    plot.plot(edge_counts, cycle_probabilities, label=f"Nodes = {x}")
    plot.ylabel("Cycle Probability")
    plot.xlabel("Number of edges")
    plot.title("Edges vs Cycle Probability")
    plot.legend()
    plot.show()

# for graph testing:
# plot_cy_p(100, 100, 100, 1)

# exp2 code:


def calc_con_p(x, n, m, step):
    connected_probabilities = []
    edge_counts = list(range(0, n+1, step))
    for j in edge_counts:
        connected_count = 0
        for i in range(m):
            G = create_random_graph(x, j)
            if is_connected(G):
                connected_count += 1

        connected_probabilities.append(connected_count / m)
    return edge_counts, connected_probabilities


def plot_con_p(x, n, m, step):
    edge_counts, connected_probabilities = calc_con_p(x, n, m, step)
    plot.plot(edge_counts, connected_probabilities, label=f"Nodes = {x}")
    plot.ylabel("Connected Probability")
    plot.xlabel("Number of edges")
    plot.title("Edges vs Connected Probability")
    plot.legend()
    plot.show()

# call for experiment 2
# plot_con_p(100, 1000, 100, 10)

# approx1 algorithm for Vertex Cover Problem


def approx1(G):
    # make copy of G [deepcopy functionality is as expected]
    graphCopy = copy.deepcopy(G)
    C = set()
    possibleVertexCover = False

    while (possibleVertexCover == False):
        # within graphCopy, find highestdegree vertex [functionality is as expected]
        v = 0
        maxDegree = 0
        for node in graphCopy.adj:
            numAdjacentNodes = len(graphCopy.adj[node])
            if numAdjacentNodes > maxDegree:
                maxDegree = numAdjacentNodes
                v = node
        C.add(v)

        # within graphCopy, remove v from the other nodes' adjacency list
        # and clear v's adjacency list [functionality is as expected ]
        for node in graphCopy.adj[v]:
            graphCopy.adj[node].remove(v)

        graphCopy.adj[v].clear()

        # check if C is a possible vertex cover for original graph, G
        possibleVertexCover = is_vertex_cover(G, C)

    return C

# approx2 algorithm for Vertex Cover Problem


def approx2(G):
    C = set()
    possibleVertexCover = False

    # set up list of vertices
    vertexList = []
    for node in G.adj:
        vertexList.append(node)

    while (possibleVertexCover == False):

        # pick a random vertex from G that's already not in C, and add it to C
        while (True):
            randomIndex = random.randint(0, len(vertexList)-1)
            chosenVertex = vertexList[randomIndex]
            if chosenVertex not in C:
                C.add(chosenVertex)
                break

        possibleVertexCover = is_vertex_cover(G, C)

    return C

# approx3 algorithm for Vertex Cover Problem
# assumption: in approx3(G), G must be a graph with at least 1 edge


def approx3(G):

    # make copy of G [deepcopy functionality is as expected]
    graphCopy = copy.deepcopy(G)
    C = set()
    possibleVertexCover = False

    while (possibleVertexCover == False):

        # within graphCopy, randomly pick an edge [works as expected]
        while (True):
            # set up list of vertices
            vertexList = []
            for node in graphCopy.adj:
                vertexList.append(node)

            # pick random vertex, u
            randomIndex = random.randint(0, len(vertexList)-1)
            u = vertexList[randomIndex]

            if len(graphCopy.adj[u]) > 0:
                # within node u's adjacency list, pick another random vertex, v
                anotherRandomIndex = random.randint(
                    0, len(graphCopy.adj[u]) - 1)
                v = graphCopy.adj[u][anotherRandomIndex]
                C.add(u)
                C.add(v)
                break

        # within graphCopy, remove u from the other nodes' adjacency list
        # and clear u's adjacency list
        for node in graphCopy.adj[u]:
            graphCopy.adj[node].remove(u)

        graphCopy.adj[u].clear()

        # within graphCopy, remove v from the other nodes' adjacency list
        # and clear v's adjacency list
        for node in graphCopy.adj[v]:
            graphCopy.adj[node].remove(v)

        graphCopy.adj[v].clear()

        # check if C is a possible vertex cover for original graph, G
        possibleVertexCover = is_vertex_cover(G, C)

    return C


# exp3 approx experiments
# utility functions


def create_copy(G):
    length = G.number_of_nodes()
    graph = Graph(length)

    for i in range(length):
        for adj_vertex in G.adj[i]:
            graph.adj[i].append(adj_vertex)

    return graph


def has_edges(G):
    for i in range(G.number_of_nodes()):
        if len(G.adj[i]) > 0:
            return True
    return False


def removeNode(G, node1):
    G.adj.pop(node1)
    for node in G.adj.keys():
        if node1 in G.adj[node]:
            G.adj[node].remove(node1)


def rand_graph(nodes, edges):
    G = Graph(nodes)
    for i in range(edges):
        while (True):
            node1, node2 = random.randint(
                0, nodes-1), random.randint(0, nodes-1)
            if not (G.are_connected(node1, node2)):
                G.add_edge(node1, node2)
                break
    return G


def performance(approx, nodes, edges):
    MVC_size = 0
    approx_size = 0
    for _ in range(0, 1000):
        G = rand_graph(nodes, edges)
        MVC_size += len(MVC(G))
        if approx == 1:
            approx_size += len(approx1(G))
        elif approx == 2:
            approx_size += len(approx2(G))
        elif approx == 3:
            approx_size += len(approx3(G))
    performance = approx_size / MVC_size
    return performance


def worst_case_performance(approx, nodes, edges):
    MVC_size = 0
    approx_size = 0
    performance = 0
    for _ in range(0, 1000):
        G = rand_graph(nodes, edges)
        MVC_size = len(MVC(G))

        if approx == 1:
            approx_size = len(approx1(G))
        elif approx == 2:
            approx_size = len(approx2(G))
        elif approx == 3:
            approx_size = len(approx3(G))
        performance = max(performance, (approx_size / MVC_size))
    print(performance)
    return performance


def MVC_exp1(nodes):
    performance1, performance2, performance3 = list(), list(), list()
    m = [1, 5, 10, 15, 30]
    print(m)
    for i in m:
        performance1.append(performance(1, nodes, i))
        performance2.append(performance(2, nodes, i))
        performance3.append(performance(3, nodes, i))

    plot.plot(m, performance1, label="approx1")
    plot.plot(m, performance2, label="approx2")
    plot.plot(m, performance3, label="approx3")

    plot.xlabel('Number of Edges')
    plot.ylabel('Performance')
    plot.title('Performance vs Num Edges')
    plot.legend(loc=1)
    plot.show()


def MVC_exp2(edge_density):
    performance1, performance2, performance3 = list(), list(), list()
    m = [4, 6, 8, 10, 12]  # num nodes
    for i in m:
        edges = (int)(i * edge_density)
        performance1.append(performance(1, i, edges))
        performance2.append(performance(2, i, edges))
        performance3.append(performance(3, i, edges))
    plot.plot(m, performance1, label="approx1")
    plot.plot(m, performance2, label="approx2")
    plot.plot(m, performance3, label="approx3")

    plot.xlabel('Number of Nodes')
    plot.ylabel('Performance')
    plot.title('Performance vs Num Nodes')
    plot.legend(loc=1)
    plot.show()


def MVC_exp3():
    nodes = 8
    m = [4, 8, 12, 16, 25, 30]
    worst_perform1, worst_perform2, worst_perform3 = list(), list(), list()
    for i in m:
        print("done")
        worst_perform1.append(worst_case_performance(1, nodes, i))
        print("done")
        worst_perform2.append(worst_case_performance(2, nodes, i))
        print("done")
        worst_perform3.append(worst_case_performance(3, nodes, i))

    print("hello")
    plot.plot(m, worst_perform1, label="approx1")
    plot.plot(m, worst_perform2, label="approx2")
    plot.plot(m, worst_perform3, label="approx3")

    plot.xlabel('Number of Edges')
    plot.ylabel('Performance')
    plot.title('Worst Case Performance vs Num Edges')
    plot.legend(loc=1)
    plot.show()

# this runs each of the experiments


# MVC_exp3()
# MVC_exp1(10)
# MVC_exp2(0.5)


# Independent set problem

# utility funcs


def is_independent_set(G, C):
    for start in C:
        for end in G.adj[start]:
            if end in C:
                return False
    return True


def max_independent_set(G):
    node = [i for i in range(G.get_size())]
    subsets = power_set(node)
    max_set = set()
    for subset in subsets:
        if is_independent_set(G, subset):
            if len(subset) > len(max_set):
                max_set = subset
    return max_set


# test case for max_independent_set
# graph7 = Graph(4)
# graph7.add_edge(0, 1)
# graph7.add_edge(0, 2)
# graph7.add_edge(1, 3)
# graph7.add_edge(2, 3)

# result = set(max_independent_set(graph7))
# expected_result = {2, 1}
# assert result == expected_result


def exp4(nodes, maxEdges):
    size_plot = []
    ttl1 = []
    ttl2 = []
    ttl3 = []

    for i in range(maxEdges+1):
        size_plot.append(i)
        Graph = create_random_graph(nodes, i)
        mVc = len(MVC(Graph))
        mIs = len(max_independent_set(Graph))
        ttl1.append(mVc)
        ttl2.append(mIs)
        ttl3.append(mVc + mIs)

    # graph the experiment
    plot.plot(size_plot, ttl1, label="MVC")
    plot.plot(size_plot, ttl2, label="MIS")
    plot.plot(size_plot, ttl3, label="MVC + MIS")

    plot.ylabel("length")
    plot.xlabel("number of edges")
    plot.title("MVC size vs MIS size")
    plot.legend()
    plot.show()

# runs the experiment4
# exp4(10, 45)

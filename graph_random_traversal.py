# Given a directed graph, write code to randomly traverse it from a beginning node to an end node.
# Output the results, e.g. A -> B -> C -> B -> D -> C -> E -> F.

# graph = {
#     "A": ["B", "C"],
#     "B": ["C", "D"],
#     "C": ["B", "E"],
#     "D": ["C"],
#     "E": ["F"],
#     "F": []
# }
# start_node = "A"
# end_node = "F"

# Algorithm:
# Create a list of visited nodes
# Start at the start node
# Add the start node to the list of visited nodes
# Loop:
#   Randomly choose an adjacent node
#   Go to that adjacent node
#   Add that adjacent node to the list of visited nodes
#   If that's the end node, stop
#   Otherwise, repeat the loop

# Example:
# Create a list of visited nodes: Empty list
# Start at the start node: A
# Add the start node to the list of visited nodes: [A]
# Loop:
#   Randomly choose an adjacent node: B
#   Go to that adjacent node: B
#   Add that adjacent node to the list of visited nodes: [A, B]
#   If that's the end node, stop -- no
#   Otherwise, repeat the loop -- yes
# Loop:
#   Randomly choose an adjacent node: C
#   Go to that adjacent node: C
#   Add that adjacent node to the list of visited nodes: [A, B, C]
#   If that's the end node, stop -- no
#   Otherwise, repeat the loop -- yes

import random
from queue import Queue


def traverse(start_node, end_node):
    path = []
    node = start_node
    while node is not end_node:
        path.append(node)
        node = node.random_adjacent()
    # Append the end node
    path.append(node)
    return path


class Node:
    def __init__(self, name: str):
        self.name = name
        self.adjacent = None
        self.marked = False

    def add_adjacents(self, adjacents: list[object]):
        self.adjacent = list(adjacents)

    def random_adjacent(self):
        random_index = random.randint(0, len(self.adjacent) - 1)
        return self.adjacent[random_index]


# graph = {
#     "A": ["B", "C"],
#     "B": ["C", "D"],
#     "C": ["B", "E"],
#     "D": ["C"],
#     "E": ["F"],
#     "F": []
# }
# start_node = "A"
# end_node = "F"

A = Node("A")
B = Node("B")
C = Node("C")
D = Node("D")
E = Node("E")
F = Node("F")

A.add_adjacents({B, C})
B.add_adjacents({C, D})
C.add_adjacents({B, E})
D.add_adjacents({C})
E.add_adjacents({F})

# Randomly traverse the graph from A to F and print the path taken

path = traverse(A, F)
print(f"{[node.name for node in path]} ({len(path)} nodes)")

# Find the most efficient path from A to F

def bfs(start_node: Node, end_node: Node) -> list[Node]:
    path_shortest = []
    adjacent:Node
    q = Queue()
    node = start_node
    node.marked = True
    q.put(node)
    while q.qsize() > 0:
        node = q.get()
        if node.adjacent:
            for adjacent in node.adjacent:
                if not adjacent.marked:
                    adjacent.marked = True
                    q.put(adjacent)
    if node is end_node:
        return path_shortest

shortest_path = bfs(A, F)
print(f"{[node.name for node in shortest_path]} ({len(shortest_path)} nodes)")

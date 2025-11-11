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


def traverse_randomly(start_node, end_node):
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

# Problem setup: Set start and end nodes
start_node = B
end_node = E

print(f"From {start_node.name} to {end_node.name}:")

# Randomly traverse the graph from start_node to end_node and print the path taken

path = traverse_randomly(start_node, end_node)
print(f"Random traversal ({len(path)} nodes): {[node.name for node in path]}")



def bfs(start_node: Node, end_node: Node) -> list[Node]:
    # Find the most efficient path from A to F
    adjacent: Node

    # Keep track of the previous node (the one before got to the current node)
    previous_nodes = {start_node: None}

    # Create a queue of nodes to visit for the breadth-first search
    q = Queue()

    # Initialize search at start node
    node = start_node
    node.marked = True

    # Start the queue by adding the start node to the queue
    q.put(node)

    # While the queue has node(s) in it
    while q.qsize() > 0:
        # Move to the next node in the queue
        node = q.get()

        # Termination condition: Found end node
        if node is end_node:
            # Prepare to output the shortest path
            path_shortest_backwards = []
            current = node
            # Trace backwards from end node to start node
            while current is not start_node:
                path_shortest_backwards.append(current)
                current = previous_nodes[current]

            # Add the start node to the path
            path_shortest_backwards.append(start_node)

            # Reverse the path to go from start to end
            path_shortest = path_shortest_backwards[::-1]

            return path_shortest
        
        # Otherwise, check for adjacent nodes and add them to the queue if not already visited
        if node.adjacent:
            for adjacent in node.adjacent:
                if not adjacent.marked:
                    adjacent.marked = True
                    q.put(adjacent)
                    previous_nodes[adjacent] = node


def get_names(my_dict):
    """Utility to display node names if exist, or None if not"""
    names_dict = {key.name if key else None: value.name if value else None for key, value in my_dict.items()}

    return names_dict


shortest_path = bfs(start_node, end_node)
print(
    f"Shortest path    ({len(shortest_path)} nodes): {[node.name for node in shortest_path]}"
)

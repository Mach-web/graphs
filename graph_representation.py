class Node(object):
    def __init__(self, value):
        self.value = value
        self.edges = []


class Edge(object):
    def __init__(self, value, node_from, node_to):
        self.value = value
        self.node_from = node_from
        self.node_to = node_to


class Graph(object):
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges

    def insert_node(self, new_node_val):
        new_node = Node(new_node_val)
        self.nodes.append(new_node)

    def insert_edge(self, new_edge_val, node_from_val, node_to_val):
        from_found = None
        to_found = None
        for node in self.nodes:
            if node_from_val == node.value:
                from_found = node
            if node_to_val == node.value:
                to_found = node
        if from_found == None:
            from_found = Node(node_from_val)
            self.nodes.append(from_found)
        if to_found == None:
            to_found = Node(node_to_val)
            self.nodes.append(to_found)
        new_edge = Edge(new_edge_val, from_found, to_found)
        from_found.edges.append(new_edge)
        to_found.edges.append(new_edge)
        self.edges.append(new_edge)

    def get_edge_list(self):
        """Don't return a list of edge objects!
        Return a list of triples that looks like this:
        (Edge Value, From Node Value, To Node Value)"""

        edge_list = []
        for edge in self.edges:
            edge_values = (edge.value, edge.node_from.value, edge.node_to.value)
            edge_list.append(edge_values)
        return edge_list

    def get_adjacency_list(self):
        """Don't return any Node or Edge objects!
        You'll return a list of lists.
        The indecies of the outer list represent
        "from" nodes.
        Each section in the list will store a list
        of tuples that looks like this:
        (To Node, Edge Value)"""
        # create an adjacency list for the nodes
        adjacency_list = []
        # Declare a variable j which only increments if index is equal to node value
        j = 0
        length_nodes = self.nodes[-1].value
        # A loop to pass through all values in nodes
        for i in range(0, len(self.nodes) + 1):
            # check if index is equal to node value
            if i == self.nodes[j].value:
                node_list = []
                for edge_in_node in self.nodes[j].edges:
                    '''
                    loop over edge value in a particular node
                    if there is an edge where node is the starting point, the node_to and edge value are appended to 
                    the list
                    '''
                    if edge_in_node.node_from == self.nodes[j]:
                        node_to_value = edge_in_node.node_to.value
                        edge_value = edge_in_node.value
                        node_list.append((node_to_value, edge_value))
                if node_list == []:
                    node_list = None
                adjacency_list.append(node_list)
                j += 1
            else:
                # append none if index and node values are not equal
                adjacency_list.append(None)
        return adjacency_list

    def get_adjacency_matrix(self):
        """Return a matrix, or 2D list.
        Row numbers represent from nodes,
        column numbers represent to nodes.
        Store the edge values in each spot,
        and a 0 if no edge exists."""
        adjacency_matrix = []
        node_index = 0
        expected_value = 0
        while self.nodes[node_index]:
            node_matrix = [0] * (len(self.nodes)+1)
            if self.nodes[node_index].value == expected_value:
                node = self.nodes[node_index]
                # edges to which the particular node is the start point
                edge_values = [i for i in self.edges if node == i.node_from]
                # loop the edges replacing to get the node_to value which you use to assign the edge value on the matrix
                for edge in edge_values:
                    node_matrix[edge.node_to.value] = edge.value

                node_index += 1
                expected_value += 1
                # append node matrix before the loop is broken
                adjacency_matrix.append(node_matrix)
                if len(self.nodes) == node_index:
                    break
            else:
                # append an empty node matrix when the expected value is not equal to node value
                adjacency_matrix.append(node_matrix)
                expected_value += 1
        return adjacency_matrix


graph = Graph()
graph.insert_edge(100, 1, 2)
graph.insert_edge(101, 1, 3)
graph.insert_edge(102, 1, 4)
graph.insert_edge(103, 3, 4)
# Should be [(100, 1, 2), (101, 1, 3), (102, 1, 4), (103, 3, 4)]
print(graph.get_edge_list())
# Should be [None, [(2, 100), (3, 101), (4, 102)], None, [(4, 103)], None]
print(graph.get_adjacency_list())
# # Should be [[0, 0, 0, 0, 0], [
# 0, 0, 100, 101, 102], [0, 0, 0, 0, 0], [0, 0, 0, 0, 103], [0, 0, 0, 0, 0]]
print(graph.get_adjacency_matrix())

class Node(object):
    def __init__(self, value):
        self.value = value
        self.edges = []
        self.visited = False


class Edge(object):
    def __init__(self, value, node_from, node_to):
        self.value = value
        self.node_from = node_from
        self.node_to = node_to


# You only need to change code with docs strings that have TODO.
# Specifically: Graph.dfs_helper and Graph.bfs
# New methods have been added to associate node numbers with names
# Specifically: Graph.set_node_names
# and the methods ending in "_names" which will print names instead
# of node numbers

class Graph(object):
    def __init__(self, nodes=None, edges=None):
        self.nodes = nodes or []
        self.edges = edges or []
        self.node_names = []
        self._node_map = {}

    def set_node_names(self, names):
        """The Nth name in names should correspond to node number N.
        Node numbers are 0 based (starting at 0).
        """
        self.node_names = list(names)

    def insert_node(self, new_node_val):
        "Insert a new node with value new_node_val"
        new_node = Node(new_node_val)
        self.nodes.append(new_node)
        self._node_map[new_node_val] = new_node
        return new_node

    def insert_edge(self, new_edge_val, node_from_val, node_to_val):
        "Insert a new edge, creating new nodes if necessary"
        nodes = {node_from_val: None, node_to_val: None}
        for node in self.nodes:
            if node.value in nodes:
                nodes[node.value] = node
                if all(nodes.values()):
                    break
        for node_val in nodes:
            nodes[node_val] = nodes[node_val] or self.insert_node(node_val)
        node_from = nodes[node_from_val]
        node_to = nodes[node_to_val]
        new_edge = Edge(new_edge_val, node_from, node_to)
        node_from.edges.append(new_edge)
        node_to.edges.append(new_edge)
        self.edges.append(new_edge)

    def get_edge_list(self):
        """Return a list of triples that looks like this:
        (Edge Value, From Node, To Node)"""
        return [(e.value, e.node_from.value, e.node_to.value)
                for e in self.edges]

    def get_edge_list_names(self):
        """Return a list of triples that looks like this:
        (Edge Value, From Node Name, To Node Name)"""
        return [(edge.value,
                 self.node_names[edge.node_from.value],
                 self.node_names[edge.node_to.value])
                for edge in self.edges]

    def get_adjacency_list(self):
        """Return a list of lists.
        The indecies of the outer list represent "from" nodes.
        Each section in the list will store a list
        of tuples that looks like this:
        (To Node, Edge Value)"""
        max_index = self.find_max_index()
        adjacency_list = [[] for _ in range(max_index)]
        for edg in self.edges:
            from_value, to_value = edg.node_from.value, edg.node_to.value
            adjacency_list[from_value].append((to_value, edg.value))
        return [a or None for a in adjacency_list]  # replace []'s with None

    def get_adjacency_list_names(self):
        """Each section in the list will store a list
        of tuples that looks like this:
        (To Node Name, Edge Value).
        Node names should come from the names set
        with set_node_names."""
        adjacency_list = self.get_adjacency_list()

        def convert_to_names(pair, graph=self):
            node_number, value = pair
            return (graph.node_names[node_number], value)

        def map_conversion(adjacency_list_for_node):
            if adjacency_list_for_node is None:
                return None
            return map(convert_to_names, adjacency_list_for_node)

        return [map_conversion(adjacency_list_for_node)
                for adjacency_list_for_node in adjacency_list]

    def get_adjacency_matrix(self):
        """Return a matrix, or 2D list.
        Row numbers represent from nodes,
        column numbers represent to nodes.
        Store the edge values in each spot,
        and a 0 if no edge exists."""
        max_index = self.find_max_index()
        adjacency_matrix = [[0] * (max_index) for _ in range(max_index)]
        for edg in self.edges:
            from_index, to_index = edg.node_from.value, edg.node_to.value
            adjacency_matrix[from_index][to_index] = edg.value
        return adjacency_matrix

    def find_max_index(self):
        """Return the highest found node number
        Or the length of the node names if set with set_node_names()."""
        if len(self.node_names) > 0:
            return len(self.node_names)
        max_index = -1
        if len(self.nodes):
            for node in self.nodes:
                if node.value > max_index:
                    max_index = node.value
        return max_index

    def find_node(self, node_number):
        "Return the node with value node_number or None"
        return self._node_map.get(node_number)

    def _clear_visited(self):
        for node in self.nodes:
            node.visited = False

    def dfs_helper(self, start_node):
        """TODO: Write the helper function for a recursive implementation
        of Depth First Search iterating through a node's edges. The
        output should be a list of numbers corresponding to the
        values of the traversed nodes.
        ARGUMENTS: start_node is the starting Node
        MODIFIES: the value of the visited property of nodes in self.nodes
        RETURN: a list of the traversed node values (integers).
        """
        ret_list = [start_node.value]
        # Your code here
        start_node.visited = True

        for edge in start_node.edges:
            if edge.node_to.visited == False:
                ret_list.extend(self.dfs_helper(edge.node_to))
        return ret_list
    def dfs(self, start_node_num):
        """Outputs a list of numbers corresponding to the traversed nodes
        in a Depth First Search.
        ARGUMENTS: start_node_num is the starting node number (integer)
        MODIFIES: the value of the visited property of nodes in self.nodes
        RETURN: a list of the node values (integers)."""
        self._clear_visited()
        start_node = self.find_node(start_node_num)
        return self.dfs_helper(start_node)

    def dfs_names(self, start_node_num):
        """Return the results of dfs with numbers converted to names."""
        return [self.node_names[num] for num in self.dfs(start_node_num)]

    def bfs(self, start_node_num):
        """TODO: Create an iterative implementation of Breadth First Search
        iterating through a node's edges. The output should be a list of
        numbers corresponding to the traversed nodes.
        ARGUMENTS: start_node_num is the node number (integer)
        MODIFIES: the value of the visited property of nodes in self.nodes
        RETURN: a list of the node values (integers)."""
        node = self.find_node(start_node_num)
        self._clear_visited()
        ret_list = [node.value]
        # Your code here
        node.visited = True
        for edge in node.edges:
            ret_list.extend([edge.node_to.value for edge in node.edges if edge.node_to.visited == False])
            node = edge.node_to
            for node in ret_list:
                node = self.find_node(node)
                node.visited = True
                # edge.node_to.visited = True


        return ret_list

    def bfs_names(self, start_node_num):
        """Return the results of bfs with numbers converted to names."""
        return [self.node_names[num] for num in self.bfs(start_node_num)]


graph = Graph()

# You do not need to change anything below this line.
# You only need to implement Graph.dfs_helper and Graph.bfs

graph.set_node_names(('Mountain View',  # 0
                      'San Francisco',  # 1
                      'London',  # 2
                      'Shanghai',  # 3
                      'Berlin',  # 4
                      'Sao Paolo',  # 5
                      'Bangalore'))  # 6

graph.insert_edge(51, 0, 1)  # MV <-> SF
graph.insert_edge(51, 1, 0)  # SF <-> MV
graph.insert_edge(9950, 0, 3)  # MV <-> Shanghai
graph.insert_edge(9950, 3, 0)  # Shanghai <-> MV
graph.insert_edge(10375, 0, 5)  # MV <-> Sao Paolo
graph.insert_edge(10375, 5, 0)  # Sao Paolo <-> MV
graph.insert_edge(9900, 1, 3)  # SF <-> Shanghai
graph.insert_edge(9900, 3, 1)  # Shanghai <-> SF
graph.insert_edge(9130, 1, 4)  # SF <-> Berlin
graph.insert_edge(9130, 4, 1)  # Berlin <-> SF
graph.insert_edge(9217, 2, 3)  # London <-> Shanghai
graph.insert_edge(9217, 3, 2)  # Shanghai <-> London
graph.insert_edge(932, 2, 4)  # London <-> Berlin
graph.insert_edge(932, 4, 2)  # Berlin <-> London
graph.insert_edge(9471, 2, 5)  # London <-> Sao Paolo
graph.insert_edge(9471, 5, 2)  # Sao Paolo <-> London
# (6) 'Bangalore' is intentionally disconnected (no edges)
# for this problem and should produce None in the
# Adjacency List, etc.

import pprint

pp = pprint.PrettyPrinter(indent=2)

print
"Edge List"
pp.pprint(graph.get_edge_list_names())

print
"\nAdjacency List"
pp.pprint(graph.get_adjacency_list_names())

print
"\nAdjacency Matrix"
pp.pprint(graph.get_adjacency_matrix())

print
"\nDepth First Search"
pp.pprint(graph.dfs_names(2))

# Should print:
# Depth First Search
# ['London', 'Shanghai', 'Mountain View', 'San Francisco', 'Berlin', 'Sao Paolo']

print
"\nBreadth First Search"
pp.pprint(graph.bfs_names(2))
# test error reporting
# pp.pprint(['Sao Paolo', 'Mountain View', 'San Fr ancisco', 'London', 'Shanghai', 'Berlin'])

# Should print:
# Breadth First Search
# ['London', 'Shanghai', 'Berlin', 'Sao Paolo', 'Mountain View', 'San Francisco']

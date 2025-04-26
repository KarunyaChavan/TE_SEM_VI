Graph_nodes = {
    'S': [('A', 3), ('D', 4)],
    'A': [('B', 4), ('D', 5)],
    'D': [('A', 5), ('E', 2)],
    'C': [],
    'B': [('C', 4), ('E', 5)],
    'E': [('F', 4), ('B', 5)],
    'F': [('G', 1)]
}

# Returns the neighbors of a node
def get_neighbors(v):
    return Graph_nodes.get(v, None)

# Heuristic function for A* algorithm
def h(n):
    H_dist = {
        'S': 11.5,
        'A': 10.1,
        'B': 5.8,
        'C': 3.4,
        'D': 9.2,
        'E': 7.1,
        'F': 3.5,
        'G': 0
    }
    return H_dist.get(n, float('inf'))

# A* algorithm to find the shortest path from start_node to stop_node
def aStarAlgo(start_node, stop_node):
    open_set = {start_node}  # Open set contains nodes to be evaluated
    closed_set = set()   # Closed set contains nodes that have already been evaluated
    g = {start_node: 0}   # g stores the cost from the start node to each node
    parents = {start_node: start_node}  # Parents to reconstruct the path
   
    while open_set:
        print("\n------------------------------------------------------------------\n")
        print("Open Set : ",open_set)
        print("Closed Set : ", closed_set)
        # Select the node with the lowest f(n) = g(n) + h(n)
        n = min(open_set, key=lambda v: g[v] + h(v))
       
        # If the destination node is reached
        if n == stop_node:
            path = []
            print("\nParents : ",parents,"\n")
            while parents[n] != n:
                path.append(n)
                n = parents[n]
            path.append(start_node)
            path.reverse()   # Reverse the path to get the correct order
            print(f'Path found: {path}')
            return path
       
        # Evaluate neighbors of the current node
        open_set.remove(n)
        closed_set.add(n)
       
        for (m, weight) in get_neighbors(n) or []:
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                parents[m] = n
                print(parents[m], " -> ", get_neighbors(n))
                g[m] = g[n] + weight
            else:
                # If a shorter path to m is found, update g and parent
                if g[m] > g[n] + weight:
                    g[m] = g[n] + weight
                    parents[m] = n
                    print(parents[m], " Back-> ", get_neighbors(n))
                    if m in closed_set: #Backtracking - Re-examining the element to search for optimal
                        closed_set.remove(m)
                        open_set.add(m)
   
    print('Path does not exist!')
    return None

# Example usage
aStarAlgo('S', 'G')
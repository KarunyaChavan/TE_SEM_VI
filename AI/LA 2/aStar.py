graph_nodes = {
    'a' : [('b',4),('c',3)],
    'b' : [('e',12),('f',5)],
    'c' : [('d',7),('e',10)],
    'd' : [('e',2)],
    'e' : [('z',5)],
    'f' : [('z',16)]
}

def get_neighbors(v):
    return graph_nodes.get(v, None)

def h(n):
    heuristics = {
        'a' : 14,
        'b' : 12,
        'c' : 11,
        'd' : 6,
        'e' : 4,
        'f' : 11,
        'z' : 0
    } 
    return heuristics.get(n, float('inf')) #dict.get(key, default)

def aStar(start_node, goal_node):
    open_set = {start_node}
    closed_set = set()
    g = {start_node : 0} #stores weight or cost
    parents = {start_node : start_node} #Parents to recontruct the path

    while(open_set):
        print("-"*30)
        print(f"Open Set : {open_set}")
        print(f"Closed Set : {closed_set}")
        n = min(open_set, key = lambda f: g[f] + h(f))

        if(n == goal_node):
            path = []
            while(parents[n]!=n): #Reaching back to start node
                path.append(n)
                n = parents[n] 
            path.append(start_node)
            path.reverse()
            print(f"Path Found : {path}")
            return path
        
        #Exploring neighbors of current node
        open_set.remove(n)
        closed_set.add(n)

        for(m, weight) in get_neighbors(n) or []:
            if m not in open_set and m not in closed_set: #Unexplored ones
                open_set.add(m)
                parents[m] = n
                g[m] = g[n] + weight #aggregating the cost upto this node
                print(f"\n{parents[m]} ----> {get_neighbors(n)}")
            else: #Already explored ones - optimal path not found
                if g[m] > g[n] + weight:
                    g[m] = g[n] + weight
                    parents[m] = n
                    print(f"{parents[m]} Back-> {get_neighbors(n)}")
                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)
    print("Path does not exist!")                        
    return None

aStar('a','z')
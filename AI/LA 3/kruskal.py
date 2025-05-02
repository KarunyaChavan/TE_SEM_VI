class Graph:
    def __init__(self, vertices):
        self.n = vertices
        self.graph = []

    def add_edge(self, u, v, cost):
        self.graph.append([u, v, cost])

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])
    
    def apply_union(self, parent, rank, x, y): #This is exactly what union does—it joins two disjoint sets (i.e., groups of connected nodes).
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]: #assigns parent, one having the lower rank becomes parent and vice versa
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1       #increment the rank

    def kruskal_algo(self):
        result = []
        i, e = 0, 0 #e = No. of edges, i = used to move to next vertices
        self.graph = sorted(self.graph, key = lambda item:item[2]) #Sorting graph on the basis cost
        parent = []
        rank = [] #rank is a heuristic used to optimize the union operation in a Disjoint Set Union (DSU) or Union-Find data structure.
        for node in range(self.n):
            parent.append(node)
            rank.append(0)
        while(e < self.n - 1):
            u, v, cost = self.graph[i] #Note : graph is sorted now so first entry would be [2,3,1]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x!= y:
                e += 1
                result.append([u, v, cost])
                self.apply_union(parent, rank, x, y)
                print(rank)
        print("\nEDGE : WEIGHT")
        for u, v, cost in result:
            print("%d - %d : %d"%(u, v, cost))

V = 6
g = Graph(V)
G = [
    [0, 4, 6, 0, 0, 0],
    [4, 0, 6, 3, 4, 0],
    [6, 6, 0, 1, 0, 0],
    [0, 3, 1, 0, 2, 3],
    [0, 4, 0, 2, 0, 7],
    [0, 0, 0, 3, 7, 0]
    ]

print("\nAdjacent Matrix for the Graph : \n")
for i in range(V):
    for j in range(V):
        print(G[i][j], end = "  ")
        if(G[i][j]!=0):
            g.add_edge(i, j, G[i][j])
    print()

g.kruskal_algo()
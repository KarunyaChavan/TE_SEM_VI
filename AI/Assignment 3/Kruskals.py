class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph= []
        
    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])
        
    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1
            
    def kruskal_algo(self):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
        print("\nEdge : Weight")
        for u, v, weight in result:
            print("%d - %d : %d" % (u, v, weight))

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

print("Adjacent Matrix for Graph : ")
for i in range(V):
    for j in range(V):
        print(G[i][j], end = " ")
    print()

for i in range(6):
     for j in range(6):
          if G[i][j]!=0:
               g.add_edge(i,j,G[i][j])

g.kruskal_algo()
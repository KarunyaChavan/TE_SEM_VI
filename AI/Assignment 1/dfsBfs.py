class Graph:
    def __init__(self, max_vertices=15):
        self.max_vertices = max_vertices
        self.n = 0  # Number of vertices
        self.adj_list = [[] for _ in range(self.max_vertices)] 
        self.labels = [None] * self.max_vertices  

    def add_vertex(self, label):
        if label in self.labels[:self.n]:
            print(f"Vertex '{label}' already exists.")
            return -1
        if self.n >= self.max_vertices:
            print("Max vertex limit reached.")
            return
        self.labels[self.n] = label
        self.n += 1

    def find_index(self, label):
        for i in range(self.n):
            if self.labels[i] == label:
                return i
        return -1

    def add_edge(self, src, dest, directed=False):
        src_idx = self.find_index(src)
        dest_idx = self.find_index(dest)
        if src_idx == -1 or dest_idx == -1:
            print(f"One or both vertices '{src}' or '{dest}' do not exist.")
            return

        self.adj_list[src_idx].append((dest_idx))
        if not directed:
            self.adj_list[dest_idx].append((src_idx))

    def display(self):
        print("\nAdjacency List:")
        for i in range(self.n):
            print(f"{self.labels[i]} -> ", end="")
            for neighbor in self.adj_list[i]:
                print(f"({self.labels[neighbor]}) -> ", end="")
            print("NULL")

    def dfs(self):
        visited = [False] * self.n
        print("\nDFS Traversal:")
        for v in range(self.n): 
            if not visited[v]:
                self._dfs_recursive(v, visited)

    def _dfs_recursive(self, v, visited):
        visited[v] = True
        print(self.labels[v], end=" ")
        for neighbor in self.adj_list[v]:
            if not visited[neighbor]:
                self._dfs_recursive(neighbor, visited)

    def bfs(self):
        visited = [False] * self.n
        print("\nBFS Traversal:")
        for v in range(self.n): 
            if not visited[v]:
                self._bfs_traversal(v, visited)

    def _bfs_traversal(self, start, visited):
        queue = [start]  
        visited[start] = True
        while queue:
            v = queue.pop(0)  
            print(self.labels[v], end=" ")
            for neighbor in self.adj_list[v]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)  

if __name__ == "__main__":
    g = Graph()

    while True:
        print("\n-_-_-_-_-_-_-_-_-_-_- MENU -_-_-_-_-_-_-_-_-_-_-\n"
              "1) Add Vertices.\n"
              "2) Add Edge.\n"
              "3) Display Adjacency List.\n"
              "4) Perform BFS.\n"
              "5) Perform DFS.\n"
              "6) Exit.")
        choice = int(input("Choose an option: "))

        if choice == 1:
            n = int(input("Enter Number of Nodes : "))
            i = 1
            while (i <= n):
                label = input(f"Enter vertex {i} label : ")
                if(g.add_vertex(label)==-1):
                    continue
                else:
                    i+=1
            directed = input("Is the graph directed? (yes/no): ").strip().lower() == "yes"
        elif choice == 2:
            src = input("Enter source vertex: ")
            dest = input("Enter destination vertex: ")
            g.add_edge(src, dest, directed=directed)
        elif choice == 3:
            g.display()
        elif choice == 4:
            g.bfs()
        elif choice == 5:
            g.dfs()
        elif choice == 6:
            break
        else:
            print("Invalid choice. Try again.")

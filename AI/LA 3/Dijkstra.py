INF = 9999999999
V = 6
G = [
    [0,4,5,0,0,0],
    [4,0,1,9,7,0],
    [5,11,0,0,3,0],
    [0,9,0,0,13,6],
    [0,7,3,13,0,6],
    [0,0,0,2,6,0]
]

dist = [INF] * V  # Distance from source to each vertex
visited = [False] * V
parent = [-1] * V

start = 0
dist[start] = 0

print("\n📊 Adjacency Matrix:\n")
for i in range(V):
    for j in range(V):
        print(G[i][j], end="  ")
    print()

for _ in range(V):
    # Pick the unvisited vertex with the smallest distance
    min_dist = INF
    u = -1
    for i in range(V):
        if not visited[i] and dist[i] < min_dist:
            min_dist = dist[i]
            u = i

    if u == -1:  # Disconnected component
        break

    visited[u] = True

    # Update distances to neighbors
    for v in range(V):
        if G[u][v] != 0 and not visited[v]:
            if dist[v] > dist[u] + G[u][v]:
                dist[v] = dist[u] + G[u][v]
                parent[v] = u

print("\n🔗 Shortest Paths from Source (Node 0):\n")
print("Node  Parent  Distance")
for i in range(V):
    print(f"{i:<5} {parent[i]:<7} {dist[i]}")

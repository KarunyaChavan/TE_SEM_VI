INF = 9999999
V = 6
G = [[0, 4, 6, 0, 0, 0],
     [4, 0, 6, 3, 4, 0],
     [6, 6, 0, 1, 0, 0],
     [0, 3, 1, 0, 2, 3],
     [0, 4, 0, 2, 0, 7],
     [0, 0, 0, 3, 7, 0]]

visited = [0, 0, 0, 0, 0, 0]
parent_and_keys = [[i,-1,-1] for i in range(V)]
no_of_edge = 0
visited[0] = True

print("Adjacent Matrix for Graph : ")
for i in range(V):
    for j in range(V):
        print(G[i][j], end = " ")
    print()
    
print("\nEdge : Weight")
while (no_of_edge < V - 1):
    minimum = INF
    x = 0
    y = 0
    for i in range(V):
        if visited[i]:
            for j in range(V):
                if ((not visited[j]) and G[i][j]):  
                    if minimum > G[i][j]:
                        minimum = G[i][j]
                        x = i
                        y = j
    print(str(x) + "-" + str(y) + "  :  " + str(G[x][y]))
    parent_and_keys[y][1] = x
    parent_and_keys[y][2] = G[x][y]
    visited[y] = True
    no_of_edge += 1


print("\nINDEX  PARENT  KEY")	
for i in range(V):
    print(parent_and_keys[i][0],"     ",parent_and_keys[i][1],"     ",parent_and_keys[i][2])
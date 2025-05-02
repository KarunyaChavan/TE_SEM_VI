import heapq

# Define the goal state
goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Calculate Manhattan Distance
def calculate_heuristics(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(state[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance

# Find the blank tile position
def find_empty_tile(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Generate valid neighbor states
def get_neighbors(state):
    neighbors = []
    x, y = find_empty_tile(state)
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # Up, Down, Right, Left
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

# Check if goal state is reached
def is_goal_state(state):
    return state == goal_state

# A* Search implementation
def aStar(start_state):
    open_set = []
    explored = []

    heapq.heappush(open_set, (calculate_heuristics(start_state), 0, start_state)) #The tuple represents (f_score, g_score, state)

    #To keep track how we got to each puzzle state - used to later to recontruct the solution path,
    parents = {tuple(map(tuple, start_state)) : None} #Converting list of lists to tuple of tuples so it can be a dict key
    
    #Storing how many moves g, we took to reach the state
    g_scores = {tuple(map(tuple, start_state)): 0}

    while open_set:
        _, g, curr_state = heapq.heappop(open_set)
        explored.append(curr_state)

        if is_goal_state(curr_state):
            path = []
            while curr_state is not None:
                path.append(curr_state)
                curr_state = parents[tuple(map(tuple, curr_state))]
            return path[::-1], "succeeded"

        for neighbor in get_neighbors(curr_state):
            neighbor_tuple = tuple(map(tuple, neighbor))
            g_score = g + 1
            #If found a new or faster way
            if neighbor_tuple not in g_scores or g_score < g_scores[neighbor_tuple]:
                g_scores[neighbor_tuple] = g_score
                parents[neighbor_tuple] = curr_state
                #Add this neighbor to the queue to be explored later
                heapq.heappush(open_set, (g_score + calculate_heuristics(neighbor), g_score, neighbor))

    return explored[-10:], "failed"

# Initial puzzle state
start_state = [
    [1, 2, 3],
    [7, 5, 4],
    [6, 0, 8]
]

# Run the solver
solution, status = aStar(start_state)

# Output results
if status == "failed":
    print("No solution found. Showing last 10 explored states:")
    for step, state in enumerate(solution, start=1):
        print(f"\nExplored State {step} (heuristic cost: {calculate_heuristics(state)})")
        for row in state:
            print(row)
else:
    print("\n✅ Solution Found")
    for step, state in enumerate(solution):
        print(f"\nStep {step} (heuristic cost: {calculate_heuristics(state)})")
        for row in state:
            print(row)

import heapq

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]  

def calculate_heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                target_x, target_y = divmod(state[i][j] - 1, 3)
                distance += abs(target_x - i) + abs(target_y - j)
    return distance

def find_empty_tile(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_neighbors(state):
    neighbors = []
    x, y = find_empty_tile(state)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def is_goal_state(state):
    return state == goal_state

def a_star(start_state):
    open_set = []
    heapq.heappush(open_set, (calculate_heuristic(start_state), 0, start_state))
    
    parents = {tuple(map(tuple, start_state)): None}
    g_scores = {tuple(map(tuple, start_state)): 0}

    while open_set:
        _, g, current_state = heapq.heappop(open_set)

        if is_goal_state(current_state):
            path = []
            while current_state is not None:
                path.append(current_state)
                current_state = parents[tuple(map(tuple, current_state))]
            return path[::-1]

        for neighbor in get_neighbors(current_state):
            neighbor_tuple = tuple(map(tuple, neighbor))
            g_score = g + 1

            if neighbor_tuple not in g_scores or g_score < g_scores[neighbor_tuple]:
                g_scores[neighbor_tuple] = g_score
                parents[neighbor_tuple] = current_state
                heapq.heappush(open_set, (g_score + calculate_heuristic(neighbor), g_score, neighbor))

    return None  # No solution found

# Example usage
start_state = [[1, 2, 3],
               [7, 0, 5],
               [4, 8, 6]]

solution = a_star(start_state)

if solution:
    print("Solution found!")
    for step, state in enumerate(solution):
        print(f"\nStep {step} (Heuristic cost: {calculate_heuristic(state)}):")
        for row in state:
            print(row)
else:
    print("No solution exists.")

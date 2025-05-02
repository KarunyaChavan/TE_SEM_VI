def selectionSort(arr):
    n = len(arr)
    for i in range(n):
        minimum_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[minimum_idx]:
                minimum_idx = j
        if minimum_idx != i:
            arr[i], arr[minimum_idx] = arr[minimum_idx], arr[i]
    return arr

unsorted = [7,1,5,3,6,2,4]
print("\nSorted Array : ",selectionSort(unsorted))

'''
A typical Greedy Best-First Search follows this outline:

Initialize: Start from the initial node.

Use a priority queue (or min-heap) ordered by heuristic value h(n).

Select the Node with the Lowest Heuristic:

Always expand the node that appears closest to the goal based on h(n).

Goal Test: If the current node is the goal, stop.

Expand Neighbors: Add neighbors to the queue (with their h(n) values).

Repeat: Go back to Step 2 until the goal is found or the queue is empty.
'''
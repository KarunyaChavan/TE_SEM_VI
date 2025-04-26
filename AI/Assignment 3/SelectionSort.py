def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        minimum_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[minimum_index]:
                minimum_index = j
        if minimum_index != i:
            arr[i], arr[minimum_index] = arr[minimum_index], arr[i]
    return arr

unsorted = []
n = int(input("Enter the number of elements: "))
print("Enter the elements one by one:")
for i in range(n):
    unsorted.append(int(input(f"Element {i + 1}: ")))

print("\nUnsorted Array:", unsorted)
sorted_array = selection_sort(unsorted)
print("Sorted Array:", sorted_array)

def linear_search(arr, key):
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return -1


data = [4, 17, 1, 9, 3]
print(linear_search(data, 9))

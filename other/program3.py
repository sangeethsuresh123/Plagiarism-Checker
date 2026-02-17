def search_element(lst, target):
    for index in range(len(lst)):
        if lst[index] == target:
            return index
    return -1

numbers = [4, 7, 1, 9, 3]
print(search_element(numbers, 9))

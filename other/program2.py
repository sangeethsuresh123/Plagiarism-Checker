def compute_fact(value):
    output = 1
    for index in range(1, value + 1):
        output *= index
    return output

number = 5
print(compute_fact(number))

def fibb(input):
    limit = input
    list = []
    for current in range(limit):
        if current == 0:
            list.append(0)
        elif current == 1:
            list.append(1)
        else:
            sum = list[current-1] + list[current-2]
            list.append(sum)
            
    print(list)

fibb(10)
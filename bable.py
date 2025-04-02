def hada_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # タプル代入で交換
    return arr

hada=[1,5,2,4,7,3]
print(hada_sort(hada))
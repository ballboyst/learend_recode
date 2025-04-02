def h_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # タプル代入で交換
    return arr

nums=[1,5,2,4,7,3]
print(h_sort(nums))
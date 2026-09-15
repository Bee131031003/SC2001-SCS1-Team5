def insertion_sort(arr, left, right):

    comparisons = 0

    for i in range(left+1, right+1):

        j = i - 1

        while j>=left:

            comparisons += 1

            if arr[j] <= arr[j+1]:
                break

            arr[j], arr[j+1] = arr[j+1], arr[j]

            j -= 1

    return comparisons


def merge(arr,temp, left, mid, right):

    comparisons = 0

    temp[left:right+1] = arr[left:right+1]

    i = left
    j = mid + 1
    k = left

    while i<=mid and j<=right:

        comparisons += 1

        if temp[i] <= temp[j]:
            arr[k] = temp[i]
            i+=1
        else:
            arr[k] = temp[j]
            j+=1

        k+=1

    while i<=mid:
        arr[k] = temp[i]
        i+=1
        k+=1
    while j <= right:
        arr[k] = temp[j]
        j+=1
        k += 1

    return comparisons  


def _merge_sort(arr, temp, left, right):

    if left >= right:
        return 0

    comparisons = 0

    mid = (left+right) // 2

    comparisons += _merge_sort(arr, temp, left, mid)

    comparisons += _merge_sort(arr, temp, mid+1, right)

    comparisons += merge(arr,temp,left,mid,right)

    return comparisons

def merge_sort(arr):

    if len(arr) <= 1:
        return 0

    temp = [0] * len(arr)

    return _merge_sort(arr, temp, 0, len(arr)-1)


def _hybrid_merge_sort(arr, temp, left, right, S):

    if left >= right:
        return 0

    size = right - left + 1

    if size <= S:
        return insertion_sort(arr,left,right)

    comparisons = 0

    mid = (left + right) // 2

    comparisons += _hybrid_merge_sort(arr, temp, left, mid, S)

    comparisons += _hybrid_merge_sort(arr, temp, mid+1, right, S)

    comparisons += merge(arr, temp, left, mid, right)

    return comparisons


def hybrid_merge_sort(arr, S):

    if S < 1:
        raise ValueError("S must be > 1")

    if len(arr) < 1:
        return 0

    temp = [0] * len(arr)

    return _hybrid_merge_sort(arr, temp, 0, len(arr)-1, S)



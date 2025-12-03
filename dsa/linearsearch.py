# dsa/searching.py

def linear_search(arr, key, value):
    """
    arr: list[dict] – each dict is a patient record
    key: column name, e.g. "name"
    value: value to search
    """
    for i, item in enumerate(arr):
        if item.get(key) == value:
            return i, item
    return -1, None

def binary_search(arr, key, value):
    """
    arr must be sorted by key (ascending).
    Returns index and item or (-1, None).
    """
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = arr[mid].get(key)
        if mid_val == value:
            return mid, arr[mid]
        elif mid_val < value:
            low = mid + 1
        else:
            high = mid - 1
    return -1, None

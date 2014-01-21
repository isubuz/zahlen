

def sort(numbers, k):
    """Sort the input list containing numbers with a maximum value of k using
    counting sort.
    """

    freq = [0] * (k + 1)  # init with zeros, +1 to account for number 0.
    for num in numbers:
        freq[num] += 1

    out = []
    for num, count in enumerate(freq):
        out.extend([num] * count)
    return out



def sort(items):
    count = len(items)
    output = items[:]

    for i in xrange(1, count):
        item = output[i]

        j = i - 1
        while item < output[j] and j >= 0:
            output[j + 1] = output[j]
            j -= 1

        output[j + 1] = item

    return output

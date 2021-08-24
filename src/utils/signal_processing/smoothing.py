
def smoothing(data, smoothing_const):

    first = (1-smoothing_const)*data[0]
    output = [first]
    i = 1
    while i < len(data):
        current = smoothing_const*output[i-1] + (1 - smoothing_const)*data[i]
        output.append(current)
        i = 1 + i


    return output

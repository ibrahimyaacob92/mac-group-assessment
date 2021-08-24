
def downsample(data, sampling_freq, f_downsample=100):
    # todo : refactor this function to accept multiple data columns
    
    if f_downsample >= sampling_freq:
        print("invalid downsampling")

    increment = int(sampling_freq/f_downsample)
    i = 0
    downsampled_data = []
    while i < len(data):
        downsampled_data.append(data[i])
        i = i + increment

    return downsampled_data

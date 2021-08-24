
def get_sampling_freq(time_series: list, assume_consistent: bool = True):
    sampling_freq = None
    if assume_consistent:
        sampling_freq = 1/(time_series[1] - time_series[0])
    else:
        # todo: do complicated stuff if to handle incoherent dataset
        pass

    return sampling_freq

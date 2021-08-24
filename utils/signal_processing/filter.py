from numpy import number
from scipy.signal import butter, filtfilt


class FILTER_OPTION():
    LOWPASS = 'lowpass'
    HIGHPASS = 'highpass'


def butter_lowpass_filter(cutoff_freq, sampling_freq, order=1):
    nyqs = 0.5*sampling_freq
    normal_cutoff_freq = cutoff_freq/nyqs
    b, a = butter(order, normal_cutoff_freq, analog=False)
    return b, a


def butter_highpass_filter(cutoff_freq, sampling_freq, order=1):
    pass


def filter_signal(data, cutoff_freq, sampling_freq, order=1, filter_type='lowpass'):
    '''
    Main function that filter signal, by default it filter low pass

    So That
    '''
    if filter_type.lower() == 'lowpass':
        b, a = butter_lowpass_filter(cutoff_freq, sampling_freq, order)

    filtered_data = filtfilt(b, a, data)
    return filtered_data

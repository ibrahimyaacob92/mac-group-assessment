from matplotlib.figure import Figure
from utils.signal_processing.smoothing import smoothing
from utils.signal_processing.downsample import downsample
from utils.file_management.open_file import open_csv
from utils.signal_processing.filter import filter_signal
from utils.signal_processing.samplingRate import get_sampling_freq
import csv

import matplotlib.pyplot as plt


class FilterSignal:
    def __init__(self) -> None:
        self.current_fp = None
        self.voltage_fp = None
        self.time_series = None
        self.voltage_series = None
        self.current_series = None
        self.sampling_freq = None
        self.filtered_voltage = None
        self.filtered_current = None
        self.downsampled_time = None
        self.downsampled_voltage = None
        self.downsampled_current = None
        self.raw_power = None
        self.smoothed_power = None

    def select_current_file(self, path):
        self.current_fp = path

    def select_voltage_file(self, path):
        self.voltage_fp = path

    def calculate_power(self, f_cutoff, f_downsample, smoothing_const):
        try:
            self._fetch_data_series()
            self._calculate_sampling_freq()
            self._filter_signal(f_cutoff)
            self._downsample_signal(f_downsample)
            self._calculate_power()
            self._smoothing_power(smoothing_const)
        except Exception as e:
            print("calculate power failed: ", e)

    def plot_chart(self, returnAsEmbeddedFig=False, formatting=None):
        fig = None
        if returnAsEmbeddedFig:
            fig = plt.figure(figsize=(10, 5), dpi=100)
            plotObj = fig.add_subplot(111)
        else:
            plotObj = plt

        try:
            plotObj.plot(self.downsampled_time,
                         self.downsampled_current, color='orange')
            plotObj.plot(self.downsampled_time,
                         self.downsampled_voltage, color='green')
            plotObj.plot(self.downsampled_time, self.raw_power,
                         label='b4 smooth', color='red')
            plotObj.plot(self.downsampled_time, self.smoothed_power,
                         label='aft smooth', color='blue')
            plotObj.legend(
                ["Current (A)", "Voltage (V)", "Raw Power (W)", "Smoothen Power (W)"])
            if returnAsEmbeddedFig:
                return fig

            plotObj.show()

        except Exception as e:
            print("plot chart failed: ", e)

    def save_csv(self, path, parameter='smoothed_power'):

        try:
            header = ['time', parameter]
            time_data = self.downsampled_time
            power_data = getattr(self, parameter)
            data = zip(time_data, power_data)
            print(power_data)
            with open(path, 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)

        except Exception as e:
            print("Error on saving CSV: ", e)

    def _fetch_data_series(self):
        voltage_data = open_csv(self.voltage_fp)
        current_data = open_csv(self.current_fp)
        voltage_time_series = voltage_data['values'][0]
        voltage_series = voltage_data['values'][1]
        current_time_series = current_data['values'][0]
        current_series = current_data['values'][1]
        # todo : check if time is valid (same lenght & same time, if true)
        self.voltage_series = voltage_series
        self.current_series = current_series
        self.time_series = voltage_time_series

        return True

    def _calculate_sampling_freq(self):
        self.sampling_freq = get_sampling_freq(self.time_series)

    def _filter_signal(self, f_cutoff):
        self.filtered_voltage = filter_signal(
            self.voltage_series, f_cutoff, self.sampling_freq)
        self.filtered_current = filter_signal(
            self.current_series, f_cutoff, self.sampling_freq)

    def _downsample_signal(self, f_downsample):

        self.downsampled_time = downsample(
            self.time_series, self.sampling_freq, f_downsample)
        self.downsampled_current = downsample(
            self.filtered_current, self.sampling_freq, f_downsample)
        self.downsampled_voltage = downsample(
            self.filtered_voltage, self.sampling_freq, f_downsample)

    def _calculate_power(self):
        power = []
        for num1, num2 in zip(self.downsampled_current, self.downsampled_voltage):
            power.append(num1 * num2)

        self.raw_power = power

    def _smoothing_power(self, smoothing_const):
        self.smoothed_power = smoothing(self.raw_power, smoothing_const)

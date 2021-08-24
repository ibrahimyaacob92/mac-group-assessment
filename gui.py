from tkinter import *
from utils.signal_processing.filter import filter_signal
from FilterSignal import FilterSignal


def run_gui():
    root = Tk()
    gui = Window(root)
    gui.root.mainloop()


class Window:

    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Signal Filter Stuff")
        self.root.geometry("1000x600")
        self.fs = FilterSignal()

        Label(self.root, text="Folder Path", anchor='w').grid(
            sticky='W', row=0, column=0)
        self.folder_path = Entry(self.root, width=50).grid(
            row=1, column=0)
        Button(self.root, text="Browse").grid(row=1, column=1)

        Label(self.root, text="Voltage File Prefix").grid(row=2, column=0)
        self.volt_prefix = Entry(self.root, width=10, textvariable=StringVar(
            self.root, 'C1'))
        self.volt_prefix.grid(row=2, column=1)

        Label(self.root, text="Current File Prefix").grid(row=3, column=0)
        self.current_prefix = Entry(self.root, width=10, textvariable=StringVar(
            self.root, 'C2'))
        self.current_prefix.grid(row=3, column=1)

        Label(self.root, text="Power File Prefix").grid(row=4, column=0)
        self.power_prefix = Entry(self.root, width=10, textvariable=StringVar(
            self.root, 'C3'))
        self.power_prefix.grid(row=4, column=1)

        Button(self.root, width=20, text="Load Files",
               command=self._handlePlot).grid(row=8, columnspan=2)

        Label(self.root, text="Frequency Cutoff").grid(row=5, column=0)
        self.f_cutoff = Entry(self.root, width=10, textvariable=DoubleVar(
            self.root, 16000))
        self.f_cutoff.grid(row=5, column=1)
        Label(self.root, text="Frequency Downsample").grid(row=6, column=0)
        self.f_downsample = Entry(self.root, width=10, textvariable=DoubleVar(
            self.root, 100))
        self.f_downsample.grid(row=6, column=1)

        Label(self.root, text="Smoothing Constant").grid(row=7, column=0)
        self.smoothing_const = Entry(self.root, width=10, textvariable=DoubleVar(
            self.root, 0.9))
        self.smoothing_const.grid(row=7, column=1)

        Button(self.root, width=20, text="Plot",
               command=self._handlePlot).grid(row=8, columnspan=2)

        Button(self.root, width=20, text="Save to CSV",
               command=self._handleSave).grid(row=9, columnspan=2)

    def _handlePlot(self):
        f_cutoff = float(self.f_cutoff.get())
        f_downsample = float(self.f_downsample.get())
        smoothing_const = float(self.smoothing_const.get())

        file_path1 = 'dataset/C1_testing.csv'
        file_path2 = 'dataset/C2_testing.csv'

        file_path1 = 'dataset/C1--ER2-JANE--00009.csv'
        file_path2 = 'dataset/C2--ER2-JANE--00009.csv'

        self.fs.select_current_file(file_path1)
        self.fs.select_voltage_file(file_path2)
        self.fs.calculate_power(f_cutoff, f_downsample, smoothing_const)
        self.fs.plot_chart()

    def _handleBrowseFile(self):

        self._handleLoadFile()
        pass

    def _handleLoadFile(self):
        # todo
        pass

    def _handleSave(self):
        self.save()


run_gui()

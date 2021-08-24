import os
from tkinter import *
from tkinter import filedialog
from FilterSignal import FilterSignal
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk, FigureCanvasTkAgg


def run_gui():
    root = Tk()
    gui = Window(root)
    gui.root.mainloop()


class Window:

    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Signal Filter Stuff")
        self.root.geometry("1500x600")
        self.browsed_dir = "desktop"
        self.target_file_extension = ".csv"
        self.voltage_file_name = None
        self.current_file_name = None
        self.fs = FilterSignal()
        self.count = 0

        # * File Browser
        # todo : loop operation on the rendered item instead of hardcoded each button
        Label(self.root, justify='left', text="Browse a folder containing 1 current source and 1 voltage source with the defined prefix", anchor='w').grid(
            row=0, column=0, columnspan=3, sticky='w', padx=(20, 0))
        self.folder_path = Entry(self.root, width=50)
        self.folder_path.grid(row=1, column=0, padx='10')
        Button(self.root, text="Browse", width=10,
               command=self._handleBrowseFile).grid(row=1, column=1)

        Label(self.root, text="Voltage File Prefix").grid(
            row=2, column=0)
        self.volt_prefix = Entry(self.root, width=10, textvariable=StringVar(
            self.root, 'C1'))
        self.volt_prefix.grid(row=2, column=1)

        Label(self.root, text="Current File Prefix").grid(row=3, column=0)
        self.current_prefix = Entry(self.root, width=10, textvariable=StringVar(
            self.root, 'C2'))
        self.current_prefix.grid(row=3, column=1)

        Label(self.root, text="Power File Prefix (For Output)").grid(
            row=4, column=0)
        self.power_prefix = Entry(self.root, width=10, textvariable=StringVar(
            self.root, 'C3'))
        self.power_prefix.grid(row=4, column=1)

        self.inspect_file_btn = Button(self.root, width=10, text="Load Files",
                                       command=self._handleLoadFile)
        self.inspect_file_btn.grid(row=5, column=1, pady=(0, 10))

        self.file_loaded_label = Label(self.root, text="**No file loaded**")
        self.file_loaded_label.grid(row=5, column=0)

        # * Calculation
        Label(self.root, text="Frequency Cutoff").grid(row=7, column=0)
        self.f_cutoff = Entry(self.root, width=10, textvariable=DoubleVar(
            self.root, 16000))
        self.f_cutoff.grid(row=7, column=1)
        Label(self.root, text="Frequency Downsample").grid(row=8, column=0)
        self.f_downsample = Entry(self.root, width=10, textvariable=DoubleVar(
            self.root, 100))
        self.f_downsample.grid(row=8, column=1)

        Label(self.root, text="Smoothing Constant").grid(row=9, column=0)
        self.smoothing_const = Entry(self.root, width=10, textvariable=DoubleVar(
            self.root, 0.9))
        self.smoothing_const.grid(row=9, column=1)

        Button(self.root, width=20, text="Plot",
               command=self._handlePlot).grid(row=10, columnspan=1)

        Button(self.root, width=20, text="Save to CSV",
               command=self._handleSave).grid(row=11, columnspan=1)

    def _handlePlot(self):
        f_cutoff = float(self.f_cutoff.get())
        f_downsample = float(self.f_downsample.get())
        smoothing_const = float(self.smoothing_const.get())

        file_path1 = self.folder_path.get() + '/' + self.current_file_name
        file_path2 = self.folder_path.get() + '/' + self.voltage_file_name

        self.fs.select_current_file(file_path1)
        self.fs.select_voltage_file(file_path2)
        self.fs.calculate_power(f_cutoff, f_downsample, smoothing_const)
        figure = self.fs.plot_chart(True)
        self.chart = FigureCanvasTkAgg(figure, self.root)
        self.chart.get_tk_widget().grid(row=1, column=3, rowspan=20, pady=10, padx=10)

        toolbarFrame = Frame(self.root)
        toolbarFrame.grid(row=0, column=3, padx=10)
        self.toolbar = NavigationToolbar2Tk(self.chart, toolbarFrame)

    def _handleBrowseFile(self):
        folder_path = filedialog.askdirectory()
        self.inspect_file_btn.configure(state="normal")
        self.folder_path.configure(
            textvariable=StringVar(self.root, folder_path))
        self._handleLoadFile()

    def _handleLoadFile(self):
        # todo: load file based on the prefix and return the user the two files
        try:
            for file in os.listdir(self.folder_path.get()):
                if file.endswith(self.target_file_extension):
                    if file.startswith(self.volt_prefix.get()):
                        self.voltage_file_name = file
                    elif file.startswith(self.current_prefix.get()):
                        self.current_file_name = file
        except:
            self.voltage_file_name = None
            self.current_file_name = None

        if (self.current_file_name and self.voltage_file_name):
            found_message = "{} Found! \n {} Found! ".format(
                self.current_file_name, self.voltage_file_name)
            self.file_loaded_label.configure(text=found_message)
            self.inspect_file_btn.configure(state="disabled")
        else:
            self.file_loaded_label.configure(text="File Not Found!")

    def _handleSave(self):
        self.save()


run_gui()

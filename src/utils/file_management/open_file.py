import csv
import matplotlib.pyplot as plt

# folder_path = 'dataset/C2--ER2-JANE--00009.csv'
folder_path = 'dataset/testing.csv'


def open_csv(path: str):
    '''
    Converts csv table, header + rows, with number into array of headers and array-in-array values
    '''
    file = open(path, 'r')
    csv_reader = csv.reader(file)

    csv_dict = {
        "headers": [],
        "values": []
    }
    for rowIdx, row in enumerate(csv_reader):
        for colIdx, cellValue in enumerate(row):
            if rowIdx == 0:
                csv_dict['headers'].append([cellValue])
                csv_dict['values'].append([])
            else:
                csv_dict['values'][colIdx].append(float(cellValue))

    return csv_dict


def find_files_in_folder(extension: str, matching_string: str):
    pass

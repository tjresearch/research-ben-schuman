import tkinter as tk
import xlrd
from joblib import dump, load
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import numpy as np
from tkinter import messagebox


def create_mapped_dict(filepath):
    workbook = xlrd.open_workbook(filepath)
    sheet = workbook.sheet_by_index(0)

    mapped_dict = {}

    for i in range(0, sheet.nrows):
        key = sheet.cell(i, 0).value
        val = int(sheet.cell(i, 1).value)

        mapped_dict[key] = val

    return mapped_dict


def run_network(region_text, disaster_text):
    svc_class = load('../Resources/model.joblib')
    region_dict = create_mapped_dict('../Resources/indexedRegions.xlsx')
    disaster_dict = create_mapped_dict('../Resources/indexedDisasters.xlsx')

    region_idx = region_dict[region_text]
    disaster_idx = disaster_dict[disaster_text]

    inputs = np.asarray([[region_idx, disaster_idx]])

    tk.messagebox.showinfo("Result", str(int(svc_class.predict(inputs)[0])) + ' People')


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=1000, height=1000)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        conversion_wb = xlrd.open_workbook('../Resources/Country to ISO3.xlsx')
        conversion_sheet = conversion_wb.sheet_by_index(0)
        conversion_dict = {}
        conversion_swapped = {}

        for i in range(0, conversion_sheet.nrows):
            full = conversion_sheet.cell(i, 0)
            short = conversion_sheet.cell(i, 1)

            conversion_dict[full] = short
            conversion_swapped[short] = full

        print(conversion_swapped.values())

        workbook = xlrd.open_workbook('../Resources/idmc_disaster_all_dataset.xlsx')
        sheet = workbook.sheet_by_index(0)
        region_list = []
        for i in range(2, sheet.nrows):
            region = sheet.cell(i, 0).value

            if region is not None:
                region = region.upper()
                if region not in region_list:
                    region_list.append(region)

        full_region_list = []

        for region in region_list:
            full_region_list.append(conversion_swapped[region])

        print(len(region_list))

        region_label = tk.Label(self, text="Pick Region (ISO3):")
        region_label.grid(row=0, column=0)

        tkvar = tk.StringVar(self.master)
        tkvar.set(region_list[0])
        region_drop = tk.OptionMenu(self, tkvar, *full_region_list)
        region_drop.grid(row=1, column=0)

        category_label = tk.Label(self, text="Pick Natural Disaster Type:")
        category_label.grid(row=2, column=0)

        tkvar2 = tk.StringVar(self.master)
        tkvar2.set("Flood")
        category = tk.OptionMenu(self, tkvar2, 'Flood', 'Extreme Temperature', 'Earthquake', 'Wet Mass Movement',
                                 'Storm', 'Dry Mass Movement', 'Drought', 'Volcanic Eruption', 'Wildfire',
                                 'Mass Movement', 'Volcanic Activity', 'Severe Winter Condition')
        category.grid(row=3, column=0)

        btn = tk.Button(self.master, text="Run Network", command=lambda:run_network(conversion_dict[tkvar.get()], tkvar2.get()))
        btn.grid(row=3, column=0)


root = tk.Tk()
app = Application(master=root)
app.configure(background='blue')
app.mainloop()

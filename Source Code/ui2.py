from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow import keras
import tkinter as tk
import xlrd
import numpy as np


def run_network(hidden, iters):
    tf.compat.v1.reset_default_graph()
    n = 1000  # Eventual parsing of datatypes, reconfiguring net right now
    # Input/output placeholder
    X = tf.compat.v1.placeholder(shape=(n, 2), dtype=tf.float64, name='X')
    y = tf.compat.v1.placeholder(shape=(n, 1), dtyle=tf.float64, name='y')

    # 3 layer model right now, 2 groups of weights

    w1 = tf.Variable(np.random.rand(2, hidden), dtype=tf.float64)
    w2 = tf.Variable(np.random.rand(hidden, 1), dtype=tf.float64)

    # nn graph

    l1 = tf.sigmoid(tf.matmul(X, w1))
    trial = tf.sigmoid(tf.matmul(l1, w2))

    # loss func

    deltas = tf.square(trial - y)
    loss = tf.reduce_sum(input_tensor=deltas)

    # train nn

    optimize = tf.compat.v1.train.GradientDescentOptimizer(0.05)
    train = optimize.minimize(loss)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=1000, height=1000)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        workbook = xlrd.open_workbook('idmc_disaster_all_dataset.xlsx')
        sheet = workbook.sheet_by_index(0)
        region_list = []
        for i in range(2, sheet.nrows):
            region = sheet.cell(i, 0).value

            if region is not None:
                region = region.upper()
                if region not in region_list:
                    region_list.append(region)

        region_label = tk.Label(self, text="Pick Region (ISO3):")
        region_label.grid(row=0, column=0)

        tkvar = tk.StringVar(self.master)
        tkvar.set(region_list[0])
        region_drop = tk.OptionMenu(self, tkvar, *region_list)
        region_drop.grid(row=1, column=0)

        category_label = tk.Label(self, text="Pick Natural Disaster Type:")
        category_label.grid(row=2, column=0)

        btn = tk.Button(self.master, text="Run Network", command=run_network)
        btn.grid(row=3, column=0)

        tkvar = tk.StringVar(self.master)
        tkvar.set("Flood")
        category = tk.OptionMenu(self, tkvar, 'Flood', 'Extreme Temperature', 'Earthquake', 'Wet Mass Movement',
                                 'Storm', 'Dry Mass Movement', 'Drought', 'Volcanic Eruption', 'Wildfire',
                                 'Mass Movement', 'Volcanic Activity', 'Severe Winter Condition')
        category.grid(row=3, column=0)


root = tk.Tk()
app = Application(master=root)
app.configure(background='blue')
app.mainloop()

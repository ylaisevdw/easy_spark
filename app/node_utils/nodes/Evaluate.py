from DataTree import Tree
from line_utils.Line import Connection
from node_utils.Node import Node
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog
import tkinter as tk
from pyspark.mllib.classification import SVMWithSGD, SVMModel
from pyspark.mllib.regression import LabeledPoint

# Note: labeled points should be 0,1 for binary class and 0 ... n for multiclass
# Labeledpoint(label, [features])
# example dataset Map: [float(x) for x in row.split(' ')]
class Evaluator(Node):
    def __init__(self, canvas, gui):
        super().__init__(canvas, "medium orchid")
        self.tag = "Evaluator"
        self.rdd = None
        self.create_node()
        self.model_node = None
        self.model_connection = None
        self.data_node = None
        self.data_connection = None
        self.label_row = None
        self.features_row = None
        self.gui = gui
        self.data_tree = Tree(["row", ["label", "predicted_label"]])

    def create_node(self):
        self.oval = self.canvas.create_oval(10, 10, 90, 90, fill=self.color)
        self.label = self.canvas.create_text(50, 50, text=self.tag, tags=self.object_id, font=self.font)

    def generate_code(self, rdd):
        pass

    def drag(self, event):
        widget = event.widget
        width, height = self.get_width_height()
        xc = max(self.canvas.coords(1)[0] - width / 2,
                 min(widget.canvasx(event.x), self.canvas.coords(1)[2] + width / 2))
        yc = max(self.canvas.coords(1)[1] - height / 2,
                 min(widget.canvasx(event.y), self.canvas.coords(1)[3] + height / 2))
        width, height = self.get_width_height()
        self.canvas.coords(self.oval, [xc - width / 2, yc - height / 2, xc + width / 2, yc + height / 2])
        self.canvas.coords(self.label, [self.get_center()[0], self.get_center()[1]])

        for edge in self.outgoing_edges:
            edge.update()
        if self.model_connection is not None:
            self.model_connection.update()
        if self.data_connection is not None:
            self.data_connection.update()

    def show_options(self):
        win = tk.Toplevel()
        win.wm_title("Model evaluation")

        options_output = [i for i in self.gui.nodes]
        output_choice = tk.StringVar()
        output_choice.set("Select model node")
        drop_down_output_format = tk.OptionMenu(win, output_choice, *options_output, command=self.set_model_node)
        drop_down_output_format.place(height=40, width=150, y=10, x=10)
        drop_down_output_format.pack()
        try:
            options_levels = [i for i in self.gui.nodes]
        except AttributeError:
            mb.showinfo("Previous node unconfigured", "We couldn't find an output structure for the previous node")
            win.destroy()
            return

        output_levels = tk.StringVar()
        output_levels.set("Select data node")
        drop_down_levels = tk.OptionMenu(win, output_levels, *options_levels, command=self.set_data_node)
        drop_down_levels.place(height=40, width=150, y=60, x=10)
        drop_down_levels.pack()

        text = tk.Message(win, text="How to retrieve the label from each row?")
        text.pack()

        l = tk.StringVar()
        label = tk.Entry(win, textvariable=l)
        if self.label_row is not None:
            l.set(self.label_row)
        label.pack()

        text_2 = tk.Message(win, text="How to retrieve the features from each row?")
        text_2.pack()

        f = tk.StringVar()
        features = tk.Entry(win, textvariable=f)
        if self.features_row is not None:
            f.set(self.features_row)
        features.pack()

        save_button = ttk.Button(win, text="Save", command=lambda: self.save_options(label.get(), features.get()))
        save_button.pack()

        b = ttk.Button(win, text="Close", command=win.destroy)
        b.place(height=40, width=100, y=100, x=10)
        b.pack()

    def set_model_node(self, model_node):
        self.model_connection = Connection(model_node, self, self.canvas)
        self.gui.lines.append(self.model_connection)
        self.model_node = model_node

    def set_data_node(self, data_node):
        self.data_connection = Connection(data_node, self, self.canvas)
        self.gui.lines.append(self.data_connection)
        self.data_node = data_node

    def save_options(self, label, features):
        if len(label) > 0:
            self.label_row = label
        if len(features) > 0:
            self.features_row = features

    def get_rdd(self):
        if self.rdd is None:
            data_rdd = self.data_node.get_rdd()
            model = self.model_node.get_rdd()
            data_rdd = eval("""data_rdd.map(lambda row: ({}, {}))""".format(self.label_row, self.features_row))
            self.rdd = data_rdd.map(lambda row: (row[0], model.predict(row[1])))
        return self.rdd

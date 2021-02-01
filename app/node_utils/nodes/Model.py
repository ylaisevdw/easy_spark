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
class Model(Node):
    def __init__(self, canvas):
        super().__init__(canvas, "MediumPurple1")
        self.tag = "Model"
        self.rdd = None
        self.model_type = None
        self.label_row = ""
        self.features_row = ""
        self.create_node()

    def create_node(self):
        self.oval = self.canvas.create_oval(10, 10, 90, 90, fill=self.color)
        self.label = self.canvas.create_text(50, 50, text=self.tag, tags=self.object_id, font=self.font)

    def show_options(self):
        win = tk.Toplevel()
        win.wm_title("Model")

        model_options = ["SVM"]
        model_choice = tk.StringVar()
        if self.model_type is None:
            model_choice.set("Select type of model")
        else:
            model_choice.set(self.model_type)

        drop_down_model_chocie = tk.OptionMenu(win, model_choice, *model_options, command=self.set_model_type)
        drop_down_model_chocie.place(height=40, width=300, y=10, x=10)
        drop_down_model_chocie.pack()

        text = tk.Message(win, text="How to retrieve the label from each row?")
        text.pack()

        l = tk.StringVar()
        label = tk.Entry(win, textvariable=l)
        if len(self.label_row) > 0:
            l.set(self.label_row)
        label.pack()

        text_2 = tk.Message(win, text="How to retrieve the features from each row?")
        text_2.pack()

        f = tk.StringVar()
        features = tk.Entry(win, textvariable=f)
        if len(self.features_row) > 0:
            f.set(self.features_row)
        features.pack()

        save_button = ttk.Button(win, text="Save", command=lambda: self.save_options(label.get(), features.get()))
        save_button.pack()

        b = ttk.Button(win, text="Close", command=win.destroy)
        b.place(height=40, width=100, y=100, x=10)
        b.pack()
        # b.grid(row=10, column=0)  
    
    def set_model_type(self, model_type):
        self.model_type = model_type
    
    def save_options(self, label, features):
        print(label, features)
        if len(label) > 0:
            self.label_row = label
        if len(features) > 0:
            self.features_row = features
        self.update()

    def update(self):
        self.canvas.delete(self.label)
        self.label = self.canvas.create_text(self.get_center()[0], self.get_center()[1], text=self.model_type,
                                             tags=self.object_id, font=self.font)

    def generate_code(self, rdd):
        rdd = eval("""rdd.map(lambda row: LabeledPoint({}, {}))""".format(self.label_row, self.features_row))
        model = SVMWithSGD.train(rdd, iterations=100)
        self.model = model
        return model


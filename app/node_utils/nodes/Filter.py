from node_utils.Node import Node
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog
import tkinter as tk

class Filter(Node):
    def __init__(self, canvas):
        super().__init__(canvas, "firebrick2")
        self.tag = "Filter"
        self.rdd = None
        self.level_of_filter = None
        self.condition = ""
        self.create_node()
        self.preparation_path = None

    def create_node(self):
        self.oval = self.canvas.create_oval(10, 10, 90, 90, fill=self.color)
        self.label = self.canvas.create_text(50, 50, text=self.tag, tags=self.object_id, font=self.font)

    def show_options(self):
        win = tk.Toplevel()
        win.wm_title("Filter condition")

        filter_options = ["Entire row", "Attribute in a row"]
        filter_choice = tk.StringVar()
        if self.level_of_filter is None:
            filter_choice.set("Select where you want to filter on")
        else:
            filter_choice.set(self.level_of_filter)

        drop_down_filter_chocie = tk.OptionMenu(win, filter_choice, *filter_options, command=self.set_level_of_filter)
        drop_down_filter_chocie.place(height=40, width=150, y=10, x=10)
        drop_down_filter_chocie.pack()

        text = tk.Message(win, text="Enter condition")
        text.pack()

        c = tk.StringVar()
        condition = tk.Entry(win, textvariable=c)
        if len(self.condition) > 0:
            c.set(self.condition)
        condition.pack()

        save_button = ttk.Button(win, text="Save", command=lambda: self.save_options(condition.get()))
        save_button.pack()

        b = ttk.Button(win, text="Close", command=win.destroy)
        b.place(height=40, width=100, y=100, x=10)
        b.pack()
        # b.grid(row=10, column=0)  

    def set_level_of_filter(self, filter_level):
        self.level_of_filter = filter_level

    def save_options(self, condition):
        if len(condition) > 0:
            self.condition = condition
        self.update()

    def update(self):
        self.canvas.delete(self.label)
        self.label = self.canvas.create_text(self.get_center()[0], self.get_center()[1], text=self.condition,
                                             tags=self.object_id, font=self.font)
        self.data_tree = self.incoming_edge.origin.data_tree

    def generate_code(self, rdd):
        if self.level_of_filter == "Attribute in a row":
            rdd = eval("""rdd.filter(lambda row: row.{})""".format(self.condition))
        else:
            rdd = eval("""rdd.filter(lambda row: {})""".format(self.condition))
        return rdd



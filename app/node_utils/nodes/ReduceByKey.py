from node_utils.Node import Node
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog
import tkinter as tk
from DataTree import Tree
import tkinter.font as font

class ReduceByKey(Node):
    def __init__(self, canvas):
        super().__init__(canvas, "sienna2")
        self.tag = "Aggregation"
        self.create_node()
        self.rdd = None
        self.function = None
        self.key = None
        self.preparation_path = None
        self.code = ""

    def create_node(self):
        self.oval = self.canvas.create_oval(10, 10, 90, 90, fill=self.color)
        self.label = self.canvas.create_text(50, 50, text=self.tag, tags=self.object_id, font=self.font)

    def show_options(self):
        win = tk.Toplevel()
        win.wm_title("Aggregate options")

        aggregation_options = ["Sum", "Count"]
        aggregation_choice = tk.StringVar()
        if self.function is None:
            aggregation_choice.set("Choose aggregation function")
        else:
            aggregation_choice.set(self.key)

        drop_down_agg_function = tk.OptionMenu(win, aggregation_choice, *aggregation_options, command=self.set_function)
        drop_down_agg_function.place(height=40, width=150, y=10, x=10)
        drop_down_agg_function.pack()

        try:
            options_levels = self.incoming_edge.origin.data_tree.contents
            options_levels.insert(0, "No key")
        except AttributeError:
            mb.showinfo("Previous node unconfigured", "We couldn't find an output structure for the previous node")
            win.destroy()
            return

        aggregation_key = tk.StringVar()
        if self.key is None:
            aggregation_key.set("Select key on which you want to aggregate")
        else:
            aggregation_key.set(self.key)

        drop_down_aggregation_key = tk.OptionMenu(win, aggregation_key, *options_levels, command=self.set_key)
        drop_down_aggregation_key.place(height=40, width=150, y=10, x=10)
        drop_down_aggregation_key.pack()

        tree_text = tk.Message(win, text="Structure of the output")
        tree_text.pack()

        tree = tk.StringVar()
        tree_text_field = tk.Entry(win, textvariable=tree)
        if self.data_tree is not None:
            tree.set(self.data_tree.str)
        tree_text_field.pack()

        save_button = ttk.Button(win, text="Save", command=lambda: self.save_options(tree_text_field.get()))
        save_button.pack()

        b = ttk.Button(win, text="Close", command=win.destroy)
        b.place(height=40, width=100, y=100, x=10)
        b.pack()
    
    def show_code(self):
        if self.code == "":
            win = tk.Toplevel()
            win.wm_title("Code")
            b = ttk.Button(win, text="Code is nog niet beschikbaar", command=win.destroy)
            b.grid(row=1, column=0)
        else:
            win = tk.Toplevel()
            win.wm_title("Aggregate code")
            text = tk.Text(win, height=10, width=80, font=font.Font(size=14))
            text.config(state="normal")
            text.insert(tk.INSERT, self.code)
            text.config(state="disabled")
            text.pack()

    def set_function(self, function):
        self.function = function
        
    def set_key(self, key):
        path = self.incoming_edge.origin.data_tree.get_path(key)
        print(path)
        if len(path) != 1:
            self.preparation_path = []
            for index, value in enumerate(path[1:]):
                self.preparation_path.append((value, path[index], simpledialog.askstring("Transition data required", "How do we obtain {} from {}?".format(value, path[index]))))
        print("Preparation path", self.preparation_path)
        self.key = key

    def save_options(self, tree_str):
        try:
            self.data_tree = Tree(tree_str)
            print("Data tree contents", self.data_tree.contents)
        except:
            mb.showinfo("Tree construction failed", "Unable to derive the structure specified, please try again.")
        self.update()

    def update(self):
        self.canvas.delete(self.label)
        self.label = self.canvas.create_text(self.get_center()[0], self.get_center()[1], text=self.function+"\n"+self.key,
                                             tags=self.object_id, font=self.font)

    def generate_code(self, rdd):
        if self.preparation_path is not None:
            for function in self.preparation_path:
                row = rdd.take(1)[0]
                result_fnc = eval("""lambda {}: {}""".format(function[1], function[2]))
                result_format = result_fnc(row)
                if isinstance(result_format, list):
                    self.code += "rdd.flatMap(lambda %s: %s) \n" %(function[1], function[2])
                    rdd = eval("""rdd.flatMap(lambda {}: {})""".format(function[1], function[2]))
                else:
                    self.code += "rdd.map(lambda %s: %s) \n" %(function[1], function[2])
                    rdd = eval("""rdd.map(lambda {}: {})""".format(function[1], function[2]))
        if self.function == "Count":
            self.code += "rdd.map(lambda %s: (%s, 1)).reduceByKey(lambda a,b: a+b) \n" %(self.key, self.key)
            rdd = eval("""rdd.map(lambda {}: ({}, 1)).reduceByKey(lambda a,b: a+b)""".format(self.key, self.key))
        else:
            raise NotImplementedError("function sum not implemented for ReduceByKey class")
        print(self.code)
        return rdd

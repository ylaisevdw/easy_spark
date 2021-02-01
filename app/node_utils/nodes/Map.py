from node_utils.Node import Node
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog
import tkinter as tk
from DataTree import Tree

class Map(Node):
    def __init__(self, canvas):
        super().__init__(canvas, "cornflower blue")
        self.tag = "Iteration over records"
        self.create_node()
        self.type = None
        self.level_of_loop = None
        self.code = ""
        self.preparation_path = None

    def create_node(self):
        self.oval = self.canvas.create_oval(10, 10, 90, 90, fill=self.color)
        self.label = self.canvas.create_text(50, 50, text=self.tag, tags=self.object_id, font=self.font)

    def show_options(self):
        win = tk.Toplevel()
        win.wm_title("For-each options")

        options_output = ["One output", "Multiple outputs"]
        output_choice = tk.StringVar()
        if self.type is None:
            output_choice.set("Select output type")
        else:
            output_choice.set(self.type)
        drop_down_output_format = tk.OptionMenu(win, output_choice, *options_output, command=self.set_type)
        drop_down_output_format.place(height=40, width=150, y=10, x=10)
        drop_down_output_format.pack()
        try:
            options_levels = self.incoming_edge.origin.data_tree.contents
        except AttributeError:
            mb.showinfo("Previous node unconfigured", "We couldn't find an output structure for the previous node")
            win.destroy()
            return
        output_levels = tk.StringVar()
        if self.level_of_loop is None:
            output_levels.set("Select level of loop")
        else:
            output_levels.set(self.level_of_loop)
        drop_down_levels = tk.OptionMenu(win, output_levels, *options_levels, command=self.set_level_of_loop)
        drop_down_levels.place(height=40, width=150, y=60, x=10)
        drop_down_levels.pack()

        text = tk.Message(win, text="Code to be executed for every [level]")
        text.pack()

        c = tk.StringVar()
        code = tk.Entry(win, textvariable=c)
        if len(self.code) > 0:
            c.set(self.code)
        code.pack()

        tree_text = tk.Message(win, text="Structure of the output")
        tree_text.pack()

        tree = tk.StringVar()
        tree_text_field = tk.Entry(win, textvariable=tree)
        if self.data_tree is not None:
            tree.set(self.data_tree.str)
        tree_text_field.pack()

        save_button = ttk.Button(win, text="Save", command=lambda: self.save_options(code.get(), tree_text_field.get()))
        save_button.pack()

        b = ttk.Button(win, text="Close", command=win.destroy)
        b.place(height=40, width=100, y=100, x=10)
        b.pack()
        # b.grid(row=10, column=0)

    def set_type(self, type):
        self.type = type

    def set_level_of_loop(self, level):
        path = self.incoming_edge.origin.data_tree.get_path(level)
        if len(path) != 1:
            self.preparation_path = []
            for index, value in enumerate(path[1:]):
                self.preparation_path.append((value, path[index], simpledialog.askstring("Transition data required", "How do we obtain {} from {}?".format(value, path[index]))))
        self.level_of_loop = level

    def save_options(self, code, tree_str):
        if len(code) > 0:
            self.code = code
        try:
            self.data_tree = Tree(tree_str)
        except:
            mb.showinfo("Tree construction failed", "Unable to derive the structure specified, please try again.")
        self.update()

    def update(self):
        self.canvas.delete(self.label)
        self.label = self.canvas.create_text(self.get_center()[0], self.get_center()[1], text=self.code,
                                             tags=self.object_id, font=self.font)

    def generate_code(self, rdd):
        if self.preparation_path is not None:
            for function in self.preparation_path:
                row = rdd.take(1)[0]
                result_fnc = eval("""lambda {}: {}""".format(function[1], function[2]))
                result_format = result_fnc(row)
                if isinstance(result_format, list):
                    rdd = eval("""rdd.flatMap(lambda {}: {})""".format(function[1], function[2]))
                else:
                    rdd = eval("""rdd.map(lambda {}: {})""".format(function[1], function[2]))
        if self.type == "One output":
            rdd = eval("""rdd.map(lambda {}: {})""".format(self.level_of_loop, self.code))
        else:
            rdd = eval("""rdd.flatMap(lambda {}: {})""".format(self.level_of_loop, self.code))
        return rdd


from node_utils.Node import Node
from tkinter import filedialog, simpledialog
from DataTree import Tree
from tkinter import messagebox as mb
import tkinter as tk
from pandastable import Table

class InputFile(Node):
    def __init__(self, canvas):
        super().__init__(canvas, "light goldenrod")
        self.directory = "/"
        self.create_node()
        self.df = None
        header = mb.askyesno("Header","Does your data include headers?")

        if header:
            self.header_sep = simpledialog.askstring("Header data required", "Enter seperator of headers")
        else:
            self.header_sep = None
            while self.data_tree is None:
                try:
                    self.data_tree = Tree(simpledialog.askstring("Header data required", "Enter structure of the data"))
                except:
                    mb.showinfo("Tree construction failed", "Unable to derive the structure specified, please try again.")

    def create_node(self):
        self.oval = self.canvas.create_oval(10, 10, 90, 90, fill=self.color)
        inputFile = filedialog.askopenfile(initialdir=self.directory)

        try:
            self.directory = inputFile.name
            self.fileName = self.directory.split("/")[-1]
            print(self.fileName)
            self.label = self.canvas.create_text(50, 50, text=self.fileName, tags=self.object_id, font=self.font)
        except AttributeError:
            self.canvas.delete(self.oval)

    def show_options(self):
        if self.df == None:
            mb.showinfo("Preview fail", "Unable to provide a preview of the data.")

        else:
            win = tk.Toplevel()
            win.wm_title("Preview data")
            minimal_pandas_df = self.df.limit(10).toPandas()
            pt = Table(win, dataframe=minimal_pandas_df)
            pt.show()

    def generate_code(self, rdd):
        raise NotImplementedError("function generate_code not implemented for InputFile class")

    def get_rdd(self):
        return self.rdd

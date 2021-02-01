from node_utils.Node import Node
from node_utils.nodes.Input import InputFile
from line_utils.Line import Connection
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog
import tkinter as tk
from DataTree import Tree

class Combiner(Node):
    def __init__(self, canvas, gui):
      self.gui = gui
      print(gui)
      self.canvas = canvas
      super().__init__(canvas, "cyan")
      self.tag = "Combiner"
      self.rdd = None
      self.create_node()
      self.type = None
      self.combine_option = None
      self.incoming_nodes = []
       
    def create_node(self):
      self.oval = self.canvas.create_oval(10, 10, 90, 90, fill=self.color)
      self.label = self.canvas.create_text(50, 50, text=self.tag, tags=self.object_id)
    
    def set_combiner_method(self, method):
      print(method)
      self.combine_method = method
      self.update()

    def show_options(self):
      win = tk.Toplevel()
      win.wm_title("Combiner options")

      try:
          self.incoming_nodes.append(self.incoming_edge.origin)
      except AttributeError:
          mb.showinfo("Previous node unconfigured", "We couldn't find the previous node")
          win.destroy()
          return

      options = [
        "Join",
        "Union",
        "Intersection"
      ]
      method = tk.StringVar()
      method.set("Pick combine method")
      drop_down_levels = tk.OptionMenu(win, method, *options, command=self.set_combiner_method)
      drop_down_levels.place(height=40, width=150, y=60, x=10)
      drop_down_levels.pack()
      save_button = ttk.Button(win, text="Save", command=lambda: self.set_combiner_method(drop_down_levels.get()))
      input_button = ttk.Button(win, text="Add file", command=self.add_file)
      input_button.pack()
      save_button.pack()

      b = ttk.Button(win, text="Close", command=win.destroy)
      b.place(height=40, width=100, y=100, x=10)
      b.pack()

    def update(self):
      self.canvas.delete(self.label)
      self.label = self.canvas.create_text(self.get_center()[0], self.get_center()[1], text=self.combine_option, tags=self.object_id)
    
    def add_file(self):
      input_node = InputFile(self.canvas)
      self.incoming_nodes.append(input_node)
      Connection(input_node, self, self.canvas)
      print(self.incoming_nodes)

    def generate_code(self, rdds, sc):
      if self.combine_option == "Join":
        pass
      elif self.combine_option == "Intersection":
        pass
      elif self.combine_option == "Union":
        rdd = sc.union(rdds)
      return rdd

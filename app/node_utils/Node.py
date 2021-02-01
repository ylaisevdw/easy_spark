import abc
from abc import ABC
import random
import string
from tkinter import ttk
import tkinter as tk
import tkinter.font as font

class Node(ABC):
    def __init__(self, canvas, color):
        self.color = color
        self.canvas = canvas
        self.previousCoordinates = (0, 0)
        self.point = 0
        self.object_id = self.get_random_string()
        self.data_tree = None
        self.rdd = None
        self.oval = 0
        self.label = 0
        self.outgoing_edges = []
        self.incoming_edge = None
        self.preparation_path = None
        self.tag = ""
        self.font = font.Font(size=14, weight='bold')

    @abc.abstractmethod
    def create_node(self):
        """Create Node"""
        pass

    def drag(self, event):
        widget = event.widget
        width, height = self.get_width_height()
        xc = max(self.canvas.coords(1)[0] - width/2,min(widget.canvasx(event.x),self.canvas.coords(1)[2] + width/2))
        yc = max(self.canvas.coords(1)[1] - height/2,min(widget.canvasx(event.y),self.canvas.coords(1)[3] + height/2))
        width, height = self.get_width_height()
        self.canvas.coords(self.oval, [xc - width/2, yc - height / 2, xc + width/2, yc + height/2])
        self.canvas.coords(self.label, [self.get_center()[0], self.get_center()[1]])

        for edge in self.outgoing_edges:
            edge.update()
        if self.incoming_edge is not None:
            self.incoming_edge.update()

    def get_center(self):
        coordinates = self.canvas.coords(self.oval)
        try:
            center = ((coordinates[0] + coordinates[2]) / 2, (coordinates[1] + coordinates[3]) / 2)
            return center
        except IndexError:
            print(coordinates, self.output)

    def get_width_height(self):
        coordinates = self.canvas.coords(self.oval)
        return coordinates[0] - coordinates[2], coordinates[1] - coordinates[3]

    def get_coordinates(self):
        coordinates = self.canvas.coords(self.oval)
        return coordinates[0], coordinates[1], coordinates[2], coordinates[3]

    def get_random_string(self, length=8):
        # Random string with the combination of lower and upper case
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def is_selected(self, label):
        if self.oval == label or self.label == label:
            return True
        else:
            return False

    def show_options(self):
        win = tk.Toplevel()
        win.wm_title("Window")

        b = ttk.Button(win, text="Opties nog niet geimplementeerd voor deze node type", command=win.destroy)
        b.grid(row=1, column=0)

    def show_code(self):
        win = tk.Toplevel()
        win.wm_title("Code")
        b = ttk.Button(win, text="Code is nog niet beschikbaar", command=win.destroy)
        b.grid(row=1, column=0)

    def delete(self):
        if self.incoming_edge is not None:
            deleted_edges = [self.incoming_edge]
        else:
            deleted_edges = []
        deleted_edges.extend(self.outgoing_edges)
        for edge in deleted_edges:
            edge.delete()
        self.canvas.delete(self.oval)
        self.canvas.delete(self.label)
        return deleted_edges


    @abc.abstractmethod
    def generate_code(self, rdd):
        """
        Generates the code associated with the current node. If we call this function on every node of the path
        and execute the resulting code sequentially, we should get the code for the functionality the user specified
        :param rdd:
        :return:
        """
        pass

    def get_rdd(self):
        if self.rdd is None:
            self.rdd = self.generate_code(self.incoming_edge.origin.get_rdd())
            print(self.tag)
        return self.rdd

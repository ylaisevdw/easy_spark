import json
from DataTree import Tree
from node_utils.Node import Node
from tkinter import filedialog
from tkinter import *

class OutputNode(Node):
    def __init__(self, canvas):
        super().__init__(canvas, "SeaGreen3")
        self.create_node()

    def create_node(self):
        self.oval = self.canvas.create_oval(10, 10, 90, 90, fill=self.color)
        self.label = self.canvas.create_text(50, 50, text="Output \n node", tags=self.object_id, font=self.font)

    def generate_code(self, rdd):
        pass

    def write_to_file(self, result):
        f = filedialog.asksaveasfile(mode='w', initialdir="/", filetypes=(("Text File","*.txt"),))
        created_file = open(f.name, "a")
        try:
            created_file.write(json.dumps(result))
        except:
            for row in result:
                if isinstance(row, str):
                    try:
                        created_file.write(row + "\n")
                    except TypeError:
                        created_file.write(json.dumps(row) + "\n")
        created_file.close()

    def get_rdd(self):
        self.rdd = self.incoming_edge.origin.get_rdd()
        result = self.rdd.collect()
        print(result[:10])
        self.write_to_file(result)
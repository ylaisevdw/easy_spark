from tkinter import *

class Connection:
    def __init__(self, origin, target, canvas):
        self.origin = origin
        self.target = target
        self.origin.outgoing_edges.append(self)
        self.target.incoming_edge = self
        self.canvas = canvas
        self.line = self.draw()

    def draw(self):
        origin_coords = self.origin.get_center()
        target_coords = self.target.get_center()
        return self.canvas.create_line(origin_coords[0]+40, origin_coords[1], target_coords[0]-40, target_coords[1],
                                       fill='black', arrow=LAST)

    def update(self):
        origin_coords = self.origin.get_center()
        target_coords = self.target.get_center()
        self.canvas.coords(self.line, [origin_coords[0]+40, origin_coords[1], target_coords[0]-40, target_coords[1]])

    def delete(self):
        self.origin.outgoing_edges.remove(self)
        self.target.incoming_edge = None
        self.canvas.delete(self.line)

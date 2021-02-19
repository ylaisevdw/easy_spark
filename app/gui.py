from tkinter import *
from pyspark import SparkContext, SparkConf, SparkFiles
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark import SparkFiles
from DataTree import Tree
from tkinter import messagebox as mb
import tkinter.font as font
from node_utils.Node import Node
from node_utils.nodes.ReduceByKey import ReduceByKey
from node_utils.nodes.Map import Map
from node_utils.nodes.Input import InputFile
from node_utils.nodes.Output import OutputNode
from node_utils.nodes.Filter import Filter
from node_utils.nodes.Combiner import Combiner
from node_utils.nodes.Model import Model
from node_utils.nodes.Evaluate import Evaluator
from line_utils.Line import Connection
from graph_utils.Graph import Graph
import os

class GUI:
    sc = SparkContext(master="local[*]", appName="gui")
    # sc = SparkContext(master="spark://spark-master:7077", appName="gui")
    spark = SparkSession.builder.appName("gui").getOrCreate()

    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(root, width=1600, height=800)
        self.canvas.pack()
        self.frame = Frame(root, width=1600, height=100).pack()
        self.buttons = {}
        self.nodes = []  # array keeping track of all nodes
        self.lines = []
        self.selectedShape = 0
        self.bind_keys()
        self.create()

    def create(self):
        buttonFont = font.Font(weight="bold", size=14)
        labelFont = font.Font(weight="bold", size = 18)
        label = Label(self.frame, text="Node creation boxes", font=labelFont)
        label.place(y=620, x=550)
        label2 = Label(self.frame, text="Configuration boxes", font=labelFont)
        label2.place(y=620, x=970)
        self.canvas.create_rectangle(10, 10, 1430, 600)
        self.buttons["input"] = Button(self.frame, text="Input", highlightbackground="light goldenrod",
                                       command=self.createInputNode, font=buttonFont)
        self.buttons["input"].place(height=40, width=120, y=660, x=350)
        # self.buttons["combine"] = Button(self.frame, text="Combine files", highlighthighlightbackground="cyan",
        #                                command=self.create_combiner_node)
        # self.buttons["combine"].place(height=40, width=120, y=740, x=350)
        self.buttons["foreach"] = Button(self.frame, text="For-each", highlightbackground="cornflower blue",
                                         command=lambda: self.create_new_node(Map), font=buttonFont)
        self.buttons["foreach"].place(height=40, width=120, y=660, x=500)
        self.buttons["reduce"] = Button(self.frame, text="Aggregate", highlightbackground="sienna2",
                                        command=lambda: self.create_new_node(ReduceByKey), font=buttonFont)
        self.buttons["reduce"].place(height=40, width=120, y=660, x=650)
        self.buttons["filter"] = Button(self.frame, text="Filter", highlightbackground="firebrick2",
                                        command=lambda: self.create_new_node(Filter), font=buttonFont)
        self.buttons["filter"].place(height=40, width=120, y=660, x=800)
        self.buttons["output"] = Button(self.frame, text="Output", highlightbackground="SeaGreen3",
                                        command=lambda: self.create_new_node(OutputNode), font=buttonFont)
        self.buttons["output"].place(height=40, width=120, y=740, x=725)
        self.buttons["model"] = Button(self.frame, text="Model", highlightbackground="MediumPurple1",
                                           command=lambda: self.create_new_node(Model), font=buttonFont)
        self.buttons["model"].place(height=40, width=120, y=740, x=425)
        self.buttons["evaluate"] = Button(self.frame, text="Evaluate", highlightbackground="medium orchid",
                                          command=lambda: self.create_new_node(Evaluator), font=buttonFont)
        self.buttons["evaluate"].place(height=40, width=120, y=740, x=575)
        self.buttons["calculate"] = Button(self.frame, text="Calculate path", highlightbackground="PaleGreen1",
                                           command=self.createDAG, font=buttonFont)
        self.buttons["calculate"].place(height=40, width=160, y=660, x=1000)
        self.buttons["options"] = Button(self.frame, text="Options", highlightbackground="snow3",
                                         command=self.show_options_dialog, font=buttonFont)
        self.buttons["options"].place(height=40, width=120, y=710, x=1000)
        self.buttons["code"] = Button(self.frame, text="Show code", highlightbackground="snow3",
                                         command=self.show_code_dialog, font=buttonFont)
        self.buttons["code"].place(height=40, width=140, y=760, x=1000)
        # self.buttons["delete"] = Button(self.frame, text="Delete", highlightbackground="green",
        #                                 command=self.delete_node)
        # self.buttons["delete"].place(height=40, width=120, y=740, x=1150)

    def bind_keys(self):
        self.canvas.bind("<Button-1>", self.select_shape)
        self.canvas.bind("<B1-Motion>", self.dragShape)

    def delete_node(self):
        deleted_edges = self.selectedShape.delete()
        self.nodes.remove(self.selectedShape)
        for edge in deleted_edges:
            self.lines.remove(edge)
        del self.selectedShape
        self.selectedShape = 0

    def show_options_dialog(self):
        if self.selectedShape != 0:
            self.selectedShape.show_options()

    def show_code_dialog(self):
        if self.selectedShape != 0:
            self.selectedShape.show_code()

    def create_new_node(self, type):
        if type == Evaluator:
            new_node = type(self.canvas, self)
        else:
            new_node = type(self.canvas)
            self.lines.append(Connection(self.selectedShape, new_node, self.canvas))
        self.nodes.append(new_node)
        self.selectedShape = new_node

    def select_shape(self, event):
        widget = event.widget
        xc = widget.canvasx(event.x)
        yc = widget.canvasx(event.y)
        try:
            select = self.canvas.find_closest(xc, yc)[0]
            for node in self.nodes:
                if node.is_selected(select):
                    self.selectedShape = node
        except IndexError:
            pass
        if isinstance(self.selectedShape, InputFile):
            self.previous_selected = self.selectedShape
            self.disableButtons(["output", "calculate", "input"])
            self.enableButtons(["foreach", "reduce", "filter", "options"])
        elif isinstance(self.selectedShape, OutputNode):
            self.disableButtons(["input", "filter", "output", "options", "foreach", "reduce"])
            self.enableButtons(["calculate"])
        elif isinstance(self.selectedShape, ReduceByKey):
            self.disableButtons(["calculate"])
            self.enableButtons(["input", "filter", "output", "options", "foreach", "reduce", "model", "code"])
        elif isinstance(self.selectedShape, int):
            self.enableButtons(self.buttons.keys())
        else:
            self.disableButtons(["calculate", "code"])
            self.enableButtons(["input", "filter", "output", "options", "foreach", "reduce", "model"])

    def dragShape(self, event):
        if isinstance(self.selectedShape, Node):
            self.selectedShape.drag(event)
        pass

    def createInputNode(self):
        self.inputNode = InputFile(self.canvas)
        self.sc.addFile(self.inputNode.directory)

        print("File has been added")
        if self.inputNode.header_sep == None:
            self.rdd = self.sc.textFile("file://" + SparkFiles.get(self.inputNode.fileName))
            df = self.spark.createDataFrame(self.rdd, StringType())
        else:
            df = self.spark.read.csv(SparkFiles.get(self.inputNode.fileName), header=True,
                                        sep=self.inputNode.header_sep)
            while self.inputNode.data_tree is None:
                try:
                    self.inputNode.data_tree = Tree(["row", df.columns])
                    print(self.inputNode.data_tree.contents)
                except:
                    mb.showinfo("Tree construction failed",
                                "Unable to derive the structure specified, please try again.")
            self.rdd = df.rdd
        self.inputNode.df = df

        self.nodes.append(self.inputNode)
        self.inputNode.rdd = self.rdd
        self.selectedShape = self.inputNode
        print("RDD created: ", self.rdd.take(10))
        self.inputFile = self.inputNode.fileName
        self.levels = self.inputNode.data_tree.contents
        self.disableButtons(["input", "filter", "output", "calculate"])

    def disableButtons(self, button_list):
        for button_key in button_list:
            self.buttons[button_key]["state"] = DISABLED

    def enableButtons(self, button_list):
        for button_key in button_list:
            self.buttons[button_key]["state"] = ACTIVE

    def createDAG(self):
        self.selectedShape.get_rdd()

if __name__ == "__main__":
    root = Tk()
    gui = GUI(root)
    root.mainloop()

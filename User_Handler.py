import pickle
import tkinter
from tkinter import *

from Grid_Editor import display_grid

global snail


def Run_Code(text):
    file = open('test1.pkl','rb')
    scene = pickle.load(file)

    steps = scene.Solve_Code(text)
    print(steps)
    display_grid(scene,additional_paint=steps['steps'])
def Request_Code():
    root = Tk()
    text = Text(width=50, height=50, bg="darkgreen", fg='white', wrap=WORD)
    text.pack()

    B = tkinter.Button(root,text="Test Code",command =lambda: Run_Code(text.get("1.0",END)))
    B.pack()
    root.mainloop()
Request_Code()
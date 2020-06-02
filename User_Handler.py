import pickle
import tkinter
from tkinter import *


def Run_Code(text):
    file = open('level.pkl','rb')
    scene = pickle.load(file)

    scene.Solve_Code(text)
def Request_Code():
    root = Tk()
    text = Text(width=50, height=50, bg="darkgreen", fg='white', wrap=WORD)
    text.pack()

    B = tkinter.Button(root,text="Test Code",command = Run_Code(text.get("1.0",END)))
    B.pack()
    root.mainloop()
Request_Code()
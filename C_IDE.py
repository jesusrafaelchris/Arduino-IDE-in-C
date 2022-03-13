from tkinter import *
import subprocess
import os
import sys
from tkinter.filedialog import asksaveasfile
import os.path
import time

# Some code here

filename = []

root = Tk()
root.geometry("500x500")
root.title("C IDE")
root.minsize(350, 350)

def redirector(inputStr):
    STDOutput.configure(state="normal")
    STDOutput.insert(INSERT, inputStr)
    STDOutput.configure(state="disabled")

def deleteText():
    STDOutput.configure(state="normal")
    STDOutput.delete('1.0', END)
    STDOutput.configure(state="disabled")

def updatefile():
    with open(filename[0],'w') as text:
        text.write(inputtxt.get("1.0", "end-1c"))


def save():
    if not filename:
        files = [('C Files', '*.c')]
        f = asksaveasfile(mode='w', defaultextension=".c")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        text2save = inputtxt.get("1.0", "end-1c") # starts from `1.0`, not `0.0`
        f.write(text2save)
        filename.clear()
        filename.insert(0,str(f.name))
        f.close()

    else:
        updatefile()


def savefile():
    if not filename:
        save()
    else:
        updatefile()


def run():
    savefile()
    deleteText()
    os.system("gcc -o out " + filename[0])
    process = subprocess.Popen(['./out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    #stdout_data,stderr_data = process.communicate()
    #errcode = process.returncode
    output = process.stdout.read()
    error = process.stderr.read()
    print(output)
    print(error)
    #Output.insert(END,str(out))
    process.kill()
    process.terminate()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
#filemenu.add_command(label="New", command=donothing)
#filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=lambda : save())
root.bind('<Command-s>', lambda event: save())
root.bind('<Control-s>', lambda event: save())
filemenu.add_command(label="Run", command=lambda : run())
root.bind('<Command-r>', lambda event: run())
root.bind('<Control-r>', lambda event: run())
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

#helpmenu = Menu(menubar, tearoff=0)
#helpmenu.add_command(label="Help Index", command=donothing)
#helpmenu.add_command(label="About...", command=donothing)
#menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

l = Label(text = "Write your code")
inputtxt = Text(root, height = 20,
				width = 110,
				bg = "white")


STDOutput = Text(root, height = 10,
                    width = 25,
                    bg = "black",
                    fg = "orange")



startcode = """#include <stdio.h>
#include <stdlib.h>


int main(void) {



	}
            """

#l.pack(fill=BOTH, expand=1)
inputtxt.pack(fill=BOTH, expand=1)
STDOutput.pack(fill=BOTH, expand=1, side = LEFT)
inputtxt.insert('1.0', startcode)
sys.stdout.write = redirector
mainloop()

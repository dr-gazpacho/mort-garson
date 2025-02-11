from tkinter import *
from tkinter import ttk

# TODO: extract into separate file that allows reading from UI like we intend to read from hardware

# Start tkinter
root = Tk()
root.title("Synthesized Synthesizer Interface")

# Create frames
content = ttk.Frame(root, padding=12)
frameHeader = ttk.Frame(content, borderwidth=5, relief="ridge", width=500, height=100)
frame9960 = ttk.Frame(frameHeader, borderwidth=5, relief="sunken", width=500, height=90)
frameFlex = ttk.Frame(content, borderwidth=5, relief="ridge", width=500, height=200)
frameLabelFlex = ttk.Frame(frameFlex, width=300, height=50)

# Create vars to store I/O values
# TODO: hook into these like we are reading from hardware
mode = IntVar(root, 1)
flex1 = IntVar(root, 0)
flex2 = IntVar(root, 0)
flex3 = IntVar(root, 0)
flex4 = IntVar(root, 0)
red = IntVar(root, 0)
blue = IntVar(root, 0)
green = IntVar(root, 0)
prox = IntVar(root, 0)

# Create Mode I/O
mode1 = ttk.Radiobutton(frameHeader, text='I', variable=mode, value=1)
mode2 = ttk.Radiobutton(frameHeader, text='II', variable=mode, value=2)
mode3 = ttk.Radiobutton(frameHeader, text='III', variable=mode, value=3)
labelMode = ttk.Label(frameHeader, text="Mode")

# Create APDS9960 I/O
# TODO: validate hardware range (0-100 is used as a proof of concept)
sliderRed = ttk.Scale(frame9960, orient=VERTICAL, length=50, from_=100, to=0, variable=red)
sliderGreen = ttk.Scale(frame9960, orient=VERTICAL, length=50, from_=100, to=0, variable=blue)
sliderBlue = ttk.Scale(frame9960, orient=VERTICAL, length=50, from_=100, to=0, variable=green)
sliderProx = ttk.Scale(frame9960, orient=VERTICAL, length=50, from_=100, to=0, variable=prox)
styleRed = ttk.Style()
styleGreen = ttk.Style()
styleBlue = ttk.Style()
styleRed.configure('Red.TLabel', foreground="red")
styleGreen.configure('Green.TLabel', foreground="green")
styleBlue.configure('Blue.TLabel', foreground="blue")
labelRed = ttk.Label(frame9960, text="R", style="Red.TLabel")
labelGreen = ttk.Label(frame9960, text="G", style="Green.TLabel")
labelBlue = ttk.Label(frame9960, text="B", style="Blue.TLabel")
labelProx = ttk.Label(frame9960, text="P")

# Create flex resistor I/O
# TODO: validate hardware range (0-100 is used as a proof of concept)
sliderFlex1 = ttk.Scale(frameFlex, orient=VERTICAL, length=200, from_=100, to=0, variable=flex1)
sliderFlex2 = ttk.Scale(frameFlex, orient=VERTICAL, length=200, from_=100, to=0, variable=flex2)
sliderFlex3 = ttk.Scale(frameFlex, orient=VERTICAL, length=200, from_=100, to=0, variable=flex3)
sliderFlex4 = ttk.Scale(frameFlex, orient=VERTICAL, length=200, from_=100, to=0, variable=flex4)
labelFlex = ttk.Label(frameLabelFlex, text="Flex Resistors")

# Set up our frame sizes
content.grid(column=0, row=0, sticky=(N, S, E, W))
frameHeader.grid(column=0, row=0, columnspan=5, rowspan=1, sticky=(N, S, E, W))
frame9960.grid(column=3, row=0, columnspan=2, rowspan=2, sticky=(N, S, E, W))
frameFlex.grid(column=0, row=1, columnspan=5, rowspan=2, sticky=(N, S, E, W))
frameLabelFlex.grid(column=0, row=1, columnspan=4, rowspan=1, sticky=(N, S, E, W))

# Position mode I/O in header frame
mode1.grid(column=0, row=0)
mode2.grid(column=1, row=0)
mode3.grid(column=2, row=0)
labelMode.grid(column=1, row=1)

# Position APDS9960 I/O in header frame
sliderRed.grid(column=0, row=0)
sliderGreen.grid(column=1, row=0)
sliderBlue.grid(column=2, row=0)
sliderProx.grid(column=3, row=0)
labelRed.grid(column=0, row=1)
labelGreen.grid(column=1, row=1)
labelBlue.grid(column=2, row=1)
labelProx.grid(column=3, row=1)

# Position flex resistor I/O in flex frame
sliderFlex1.grid(column=0, row=0)
sliderFlex2.grid(column=1, row=0)
sliderFlex3.grid(column=2, row=0)
sliderFlex4.grid(column=3, row=0)
labelFlex.grid(column=0, row=0)

# set up some grid weights. This should let us get some responsive resizing, but I've messed it up somewhere
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frameHeader.columnconfigure(0, weight=1)
frameHeader.columnconfigure(1, weight=1)
frameHeader.columnconfigure(2, weight=1)
frameHeader.columnconfigure(3, weight=1)
frameHeader.columnconfigure(4, weight=1)
frameHeader.rowconfigure(0, weight=2)
frameHeader.rowconfigure(1, weight=1)

frame9960.columnconfigure(0, weight=1)
frame9960.columnconfigure(1, weight=1)
frame9960.columnconfigure(2, weight=1)
frame9960.columnconfigure(3, weight=1)
frame9960.rowconfigure(0, weight=2)
frame9960.rowconfigure(1, weight=1)

frameFlex.columnconfigure(0, weight=1)
frameFlex.columnconfigure(1, weight=1)
frameFlex.columnconfigure(2, weight=1)
frameFlex.columnconfigure(3, weight=1)
frameFlex.rowconfigure(0, weight=3)

frameLabelFlex.columnconfigure(0, weight=4)
frameLabelFlex.rowconfigure(0, weight=1)


# mainloop blocks, update_idletasks & update let us perform the same steps while hooking into the loop
# root.mainloop()
while True:
    print('mode', mode.get())
    print('rgbp', red.get(), green.get(), blue.get(), prox.get())
    print('flex', flex1.get(), flex2.get(), flex3.get(), flex4.get())
    print()
    root.update_idletasks()
    root.update()
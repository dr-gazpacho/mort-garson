from tkinter import *
from tkinter import ttk
from package.inputs.input_base import InputBase
from package.types import InputResult

# Class that creates a virtual I/O interface
class InputSimulated(InputBase):
  # https://learn.adafruit.com/adafruit-apds9960-breakout/circuitpython#color-reading-2980832
  APDS_COLOR_MIN = 0
  APDS_COLOR_MAX = 65535
  
  # https://learn.adafruit.com/adafruit-apds9960-breakout/circuitpython#proximity-reading-2980819
  APDS_PROXIMITY_MIN = 0
  APDS_PROXIMITY_MAX = 255

  # https://www.adafruit.com/product/182
  FLEX_MIN = 10000
  FLEX_MAX = 20000

  # Constructor sets up Tkinter and variables to use for polling
  def __init__(self):
    self.tkRoot = Tk()
    self.tkRoot.title=('InputSimulated')
    self.mode = IntVar(self.tkRoot, 1)
    self.flex1 = IntVar(self.tkRoot, self.FLEX_MIN)
    self.flex2 = IntVar(self.tkRoot, self.FLEX_MIN)
    self.flex3 = IntVar(self.tkRoot, self.FLEX_MIN)
    self.flex4 = IntVar(self.tkRoot, self.FLEX_MIN)
    self.red = IntVar(self.tkRoot, self.APDS_COLOR_MIN)
    self.blue = IntVar(self.tkRoot, self.APDS_COLOR_MIN)
    self.green = IntVar(self.tkRoot, self.APDS_COLOR_MIN)
    self.clear = IntVar(self.tkRoot, self.APDS_COLOR_MIN)
    self.prox = IntVar(self.tkRoot, self.APDS_PROXIMITY_MIN)
  
  # Set up virtual interface
  def setup(self) -> None:
    # Create frames
    content = ttk.Frame(self.tkRoot, padding=12)
    frameHeader = ttk.Frame(content, borderwidth=5, relief="ridge", width=500, height=100)
    frame9960 = ttk.Frame(frameHeader, borderwidth=5, relief="sunken", width=500, height=90)
    frameFlex = ttk.Frame(content, borderwidth=5, relief="ridge", width=500, height=200)
    frameLabelFlex = ttk.Frame(frameFlex, width=300, height=50)

    # Create Mode I/O
    mode1 = ttk.Radiobutton(frameHeader, text='I', variable=self.mode, value=1)
    mode2 = ttk.Radiobutton(frameHeader, text='II', variable=self.mode, value=2)
    mode3 = ttk.Radiobutton(frameHeader, text='III', variable=self.mode, value=3)
    labelMode = ttk.Label(frameHeader, text="Mode")

    # Create APDS9960 I/O
    sliderRed = ttk.Scale(frame9960, orient=VERTICAL, length=50, from_=self.APDS_COLOR_MAX, to=self.APDS_COLOR_MIN, variable=self.red)
    sliderGreen = ttk.Scale(frame9960, orient=VERTICAL, length=50, from_=self.APDS_COLOR_MAX, to=self.APDS_COLOR_MIN, variable=self.blue)
    sliderBlue = ttk.Scale(frame9960, orient=VERTICAL, length=50, from_=self.APDS_COLOR_MAX, to=self.APDS_COLOR_MIN, variable=self.green)
    sliderClear = ttk.Scale(frame9960, orient=VERTICAL, length=50, from_=self.APDS_COLOR_MAX, to=self.APDS_COLOR_MIN, variable=self.clear)
    sliderProx = ttk.Scale(frame9960, orient=VERTICAL, length=50, from_=self.APDS_PROXIMITY_MAX, to=self.APDS_PROXIMITY_MIN, variable=self.prox)
    styleRed = ttk.Style()
    styleGreen = ttk.Style()
    styleBlue = ttk.Style()
    styleRed.configure('Red.TLabel', foreground="red")
    styleGreen.configure('Green.TLabel', foreground="green")
    styleBlue.configure('Blue.TLabel', foreground="blue")
    labelRed = ttk.Label(frame9960, text="R", style="Red.TLabel")
    labelGreen = ttk.Label(frame9960, text="G", style="Green.TLabel")
    labelBlue = ttk.Label(frame9960, text="B", style="Blue.TLabel")
    labelClear = ttk.Label(frame9960, text="C")
    labelProx = ttk.Label(frame9960, text="P")

    # Create flex resistor I/O
    sliderFlex1 = ttk.Scale(frameFlex, orient=VERTICAL, length=200, from_=self.FLEX_MAX, to=self.FLEX_MIN, variable=self.flex1)
    sliderFlex2 = ttk.Scale(frameFlex, orient=VERTICAL, length=200, from_=self.FLEX_MAX, to=self.FLEX_MIN, variable=self.flex2)
    sliderFlex3 = ttk.Scale(frameFlex, orient=VERTICAL, length=200, from_=self.FLEX_MAX, to=self.FLEX_MIN, variable=self.flex3)
    sliderFlex4 = ttk.Scale(frameFlex, orient=VERTICAL, length=200, from_=self.FLEX_MAX, to=self.FLEX_MIN, variable=self.flex4)
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
    sliderClear.grid(column=3, row=0)
    sliderProx.grid(column=4, row=0)
    labelRed.grid(column=0, row=1)
    labelGreen.grid(column=1, row=1)
    labelBlue.grid(column=2, row=1)
    labelClear.grid(column=3, row=1)
    labelProx.grid(column=4, row=1)

    # Position flex resistor I/O in flex frame
    sliderFlex1.grid(column=0, row=0)
    sliderFlex2.grid(column=1, row=0)
    sliderFlex3.grid(column=2, row=0)
    sliderFlex4.grid(column=3, row=0)
    labelFlex.grid(column=0, row=0)

    # set up some grid weights. This should let us get some responsive resizing, but I've messed it up somewhere
    self.tkRoot.columnconfigure(0, weight=1)
    self.tkRoot.rowconfigure(0, weight=1)

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
    frame9960.columnconfigure(4, weight=1)
    frame9960.rowconfigure(0, weight=2)
    frame9960.rowconfigure(1, weight=1)

    frameFlex.columnconfigure(0, weight=1)
    frameFlex.columnconfigure(1, weight=1)
    frameFlex.columnconfigure(2, weight=1)
    frameFlex.columnconfigure(3, weight=1)
    frameFlex.rowconfigure(0, weight=3)

    frameLabelFlex.columnconfigure(0, weight=4)
    frameLabelFlex.rowconfigure(0, weight=1)    

  # Retrieve values and update/refresh interface
  def poll(self) -> InputResult:
    # Update Tkinter UI
    self.tkRoot.update_idletasks()
    self.tkRoot.update()

    # Return stored results    
    return (self.mode.get(), self.red.get(), self.green.get(), self.blue.get(), self.clear.get(), self.prox.get(), self.flex1.get(), self.flex2.get(), self.flex3.get(), self.flex4.get())
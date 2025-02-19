
from pythonosc import udp_client
from enum import Enum
import tkinter as tk
from tkinter import ttk
import math
import time

class DroneMode:

    def __init__(self):
        # Globals
        # https://learn.adafruit.com/adafruit-apds9960-breakout/circuitpython#color-reading-2980832
        self.APDS_COLOR_MIN = 0
        self.APDS_COLOR_MAX = 65535
        
        # https://learn.adafruit.com/adafruit-apds9960-breakout/circuitpython#proximity-reading-2980819
        self.APDS_PROXIMITY_MIN = 0
        self.APDS_PROXIMITY_MAX = 255

        # https://www.adafruit.com/product/182
        self.FLEX_MIN = 10000
        self.FLEX_MAX = 20000
        # Initialize GUI
        self.tkRoot = tk.Tk()
        self.tkRoot.title=('InputSimulated')
        self.mode = tk.IntVar(self.tkRoot, 1)
        self.flex1 = tk.IntVar(self.tkRoot, self.FLEX_MIN)
        self.flex2 = tk.IntVar(self.tkRoot, self.FLEX_MIN)
        self.flex3 = tk.IntVar(self.tkRoot, self.FLEX_MIN)
        self.flex4 = tk.IntVar(self.tkRoot, self.FLEX_MIN)
        self.red = tk.IntVar(self.tkRoot, self.APDS_COLOR_MIN)
        self.blue = tk.IntVar(self.tkRoot, self.APDS_COLOR_MIN)
        self.green = tk.IntVar(self.tkRoot, self.APDS_COLOR_MIN)
        self.clear = tk.IntVar(self.tkRoot, self.APDS_COLOR_MIN)
        self.prox = tk.IntVar(self.tkRoot, self.APDS_PROXIMITY_MIN)

        ## GUI
        # Create frames
        self.content = ttk.Frame(self.tkRoot, padding=12)
        self.frameHeader = ttk.Frame(self.content, borderwidth=5, relief="ridge", width=500, height=100)
        self.frame9960 = ttk.Frame(self.frameHeader, borderwidth=5, relief="sunken", width=500, height=90)
        self.frameFlex = ttk.Frame(self.content, borderwidth=5, relief="ridge", width=500, height=200)
        self.frameLabelFlex = ttk.Frame(self.frameFlex, width=300, height=50)

        # Create Mode I/O
        self.mode1 = ttk.Radiobutton(self.frameHeader, text='I', variable=self.mode, value=1)
        self.mode2 = ttk.Radiobutton(self.frameHeader, text='II', variable=self.mode, value=2)
        self.mode3 = ttk.Radiobutton(self.frameHeader, text='III', variable=self.mode, value=3)
        self.labelMode = ttk.Label(self.frameHeader, text="Mode")

        # Create APDS9960 I/O
        self.sliderRed = ttk.Scale(self.frame9960, orient=tk.VERTICAL, length=50, from_=self.APDS_COLOR_MAX, to=self.APDS_COLOR_MIN, variable=self.red, command=self.forward_all_values)
        self.sliderGreen = ttk.Scale(self.frame9960, orient=tk.VERTICAL, length=50, from_=self.APDS_COLOR_MAX, to=self.APDS_COLOR_MIN, variable=self.blue, command=self.forward_all_values)
        self.sliderBlue = ttk.Scale(self.frame9960, orient=tk.VERTICAL, length=50, from_=self.APDS_COLOR_MAX, to=self.APDS_COLOR_MIN, variable=self.green, command=self.forward_all_values)
        self.sliderClear = ttk.Scale(self.frame9960, orient=tk.VERTICAL, length=50, from_=self.APDS_COLOR_MAX, to=self.APDS_COLOR_MIN, variable=self.clear, command=self.forward_all_values)
        self.sliderProx = ttk.Scale(self.frame9960, orient=tk.VERTICAL, length=50, from_=self.APDS_PROXIMITY_MAX, to=self.APDS_PROXIMITY_MIN, variable=self.prox, command=self.forward_all_values)
        self.styleRed = ttk.Style()
        self.styleGreen = ttk.Style()
        self.styleBlue = ttk.Style()
        self.styleRed.configure('Red.TLabel', foreground="red")
        self.styleGreen.configure('Green.TLabel', foreground="green")
        self.styleBlue.configure('Blue.TLabel', foreground="blue")
        self.labelRed = ttk.Label(self.frame9960, text="R", style="Red.TLabel")
        self.labelGreen = ttk.Label(self.frame9960, text="G", style="Green.TLabel")
        self.labelBlue = ttk.Label(self.frame9960, text="B", style="Blue.TLabel")
        self.labelClear = ttk.Label(self.frame9960, text="C")
        self.labelProx = ttk.Label(self.frame9960, text="P")

        # Create flex resistor I/O
        self.sliderFlex1 = ttk.Scale(self.frameFlex, orient=tk.VERTICAL, length=200, from_=self.FLEX_MAX, to=self.FLEX_MIN, variable=self.flex1)
        self.sliderFlex2 = ttk.Scale(self.frameFlex, orient=tk.VERTICAL, length=200, from_=self.FLEX_MAX, to=self.FLEX_MIN, variable=self.flex2)
        self.sliderFlex3 = ttk.Scale(self.frameFlex, orient=tk.VERTICAL, length=200, from_=self.FLEX_MAX, to=self.FLEX_MIN, variable=self.flex3)
        self.sliderFlex4 = ttk.Scale(self.frameFlex, orient=tk.VERTICAL, length=200, from_=self.FLEX_MAX, to=self.FLEX_MIN, variable=self.flex4)
        self.labelFlex = ttk.Label(self.frameLabelFlex, text="Flex Resistors")

        # Set up our frame sizes
        self.content.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frameHeader.grid(column=0, row=0, columnspan=5, rowspan=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frame9960.grid(column=3, row=0, columnspan=2, rowspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frameFlex.grid(column=0, row=1, columnspan=5, rowspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frameLabelFlex.grid(column=0, row=1, columnspan=4, rowspan=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Position mode I/O in header frame
        self.mode1.grid(column=0, row=0)
        self.mode2.grid(column=1, row=0)
        self.mode3.grid(column=2, row=0)
        self.labelMode.grid(column=1, row=1)

        # Position APDS9960 I/O in header frame
        self.sliderRed.grid(column=0, row=0)
        self.sliderGreen.grid(column=1, row=0)
        self.sliderBlue.grid(column=2, row=0)
        self.sliderClear.grid(column=3, row=0)
        self.sliderProx.grid(column=4, row=0)
        self.labelRed.grid(column=0, row=1)
        self.labelGreen.grid(column=1, row=1)
        self.labelBlue.grid(column=2, row=1)
        self.labelClear.grid(column=3, row=1)
        self.labelProx.grid(column=4, row=1)

        # Position flex resistor I/O in flex frame
        self.sliderFlex1.grid(column=0, row=0)
        self.sliderFlex2.grid(column=1, row=0)
        self.sliderFlex3.grid(column=2, row=0)
        self.sliderFlex4.grid(column=3, row=0)
        self.labelFlex.grid(column=0, row=0)

        # set up some grid weights. This should let us get some responsive resizing, but I've messed it up somewhere
        self.tkRoot.columnconfigure(0, weight=1)
        self.tkRoot.rowconfigure(0, weight=1)

        self.frameHeader.columnconfigure(0, weight=1)
        self.frameHeader.columnconfigure(1, weight=1)
        self.frameHeader.columnconfigure(2, weight=1)
        self.frameHeader.columnconfigure(3, weight=1)
        self.frameHeader.columnconfigure(4, weight=1)
        self.frameHeader.rowconfigure(0, weight=2)
        self.frameHeader.rowconfigure(1, weight=1)

        self.frame9960.columnconfigure(0, weight=1)
        self.frame9960.columnconfigure(1, weight=1)
        self.frame9960.columnconfigure(2, weight=1)
        self.frame9960.columnconfigure(3, weight=1)
        self.frame9960.columnconfigure(4, weight=1)
        self.frame9960.rowconfigure(0, weight=2)
        self.frame9960.rowconfigure(1, weight=1)

        self.frameFlex.columnconfigure(0, weight=1)
        self.frameFlex.columnconfigure(1, weight=1)
        self.frameFlex.columnconfigure(2, weight=1)
        self.frameFlex.columnconfigure(3, weight=1)
        self.frameFlex.rowconfigure(0, weight=3)

        self.frameLabelFlex.columnconfigure(0, weight=4)
        self.frameLabelFlex.rowconfigure(0, weight=1)    

        # Constant to describe "mode", should be variable controlled by knob
        self.mode_enum = Enum('Mode', [('DRONE', 1), ('MODE_TWO', 2), ('MODE_THREE', 3)])
        self.mode = self.mode_enum.DRONE

        ## OSC
        self.client = udp_client.SimpleUDPClient("127.0.0.1", 57120)



        self.tkRoot.mainloop()

    def name_greatest_color(self, index):
        match index:
            case 0:
                return "red"
            case 1:
                return "green"
            case 2:
                return "blue"

    def forward_all_values(self, _=None):
        # red_value = self.red_slider.get()
        # blue_value = self.blue_slider.get()
        # green_value = self.green_slider.get()
        # clear_value = self.clear_slider.get()
        # volume_value = self.volume_slider.get()
        # is_checked = self.check_state.get() == 1

        red_two = self.sliderRed.get()
        print(red_two)

        # # some trivial computes before we send
        # vals_as_list = [red_value, green_value, blue_value]

        # index = 0
        # current_max_value = vals_as_list[index]
        # for i in range(1, len(vals_as_list)):
        #     if vals_as_list[i] > current_max_value:
        #         current_max_value = vals_as_list[i]
        #         index = i

        
        # greatest_color = self.name_greatest_color(index)
        # clear_as_single_digit = math.floor(clear_value / 10)

        # # A strategy: if drone_mode is enabled, send messages to /drone_mode OSC listener e.g. if mode.x_mode -> /x_mode elif mode.y_mode -> /y_mode
        # if self.mode == self.mode_enum.DRONE:
        #     self.client.send_message("/drone_mode", [red_value, blue_value, green_value, clear_value, volume_value, is_checked, clear_as_single_digit, greatest_color])



DroneMode()

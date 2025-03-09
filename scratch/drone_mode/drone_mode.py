from pythonosc import udp_client
from enum import Enum
import tkinter as tk
from tkinter import ttk
import argparse
import math
import time

class DroneMode:

    def __init__(self, start_gui=True, print_read_values=False):
        # Command line args
        self.print_read_values=print_read_values
        

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

        self.VOLUME_MIN = -40
        self.VOLUME_MAX = 6

        # OSC
        self.client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

        if start_gui:
            self.initialize_gui()

    def initialize_gui(self):
        """use globals to initialize the GUI and launch"""
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
        self.white = tk.IntVar(self.tkRoot, self.APDS_COLOR_MIN)
        self.prox = tk.IntVar(self.tkRoot, self.APDS_PROXIMITY_MIN)
        self.volume = tk.IntVar(self.tkRoot, 0)
        
        # Create frames
        self.content = ttk.Frame(self.tkRoot, padding=12)
        self.frameHeader = ttk.Frame(self.content, borderwidth=5, relief="ridge", width=500, height=100)
        self.frame9960 = ttk.Frame(self.frameHeader, borderwidth=5, relief="sunken", width=500, height=90)
        self.frameFlex = ttk.Frame(self.content, borderwidth=5, relief="ridge", width=500, height=200)
        self.frameLabelFlex = ttk.Frame(self.frameFlex, width=300, height=50)

        # Create Mode I/O
        self.mode1 = ttk.Radiobutton(self.frameHeader, text='I', variable=self.mode, value=1, command=self.forward_all_values)
        self.mode2 = ttk.Radiobutton(self.frameHeader, text='II', variable=self.mode, value=2, command=self.forward_all_values)
        self.mode3 = ttk.Radiobutton(self.frameHeader, text='III', variable=self.mode, value=3, command=self.forward_all_values)
        self.volume = ttk.Scale(self.frameHeader, orient=tk.VERTICAL, from_=self.VOLUME_MAX, to=self.VOLUME_MIN, variable=self.volume, length=50, command=self.forward_all_values)
        self.label_volume = ttk.Label(self.frameHeader, text="vol")

        self.labelMode = ttk.Label(self.frameHeader, text="Mode")

        # Create APDS9960 I/O
        self.sliderRed = ttk.Scale(self.frame9960, orient=tk.VERTICAL, length=50, from_=self.APDS_COLOR_MAX, to=self.APDS_COLOR_MIN, variable=self.red, command=self.forward_all_values)
        self.sliderGreen = ttk.Scale(self.frame9960, orient=tk.VERTICAL, length=50, from_=self.APDS_COLOR_MAX, to=self.APDS_COLOR_MIN, variable=self.blue, command=self.forward_all_values)
        self.sliderBlue = ttk.Scale(self.frame9960, orient=tk.VERTICAL, length=50, from_=self.APDS_COLOR_MAX, to=self.APDS_COLOR_MIN, variable=self.green, command=self.forward_all_values)
        self.sliderWhite = ttk.Scale(self.frame9960, orient=tk.VERTICAL, length=50, from_=self.APDS_COLOR_MAX, to=self.APDS_COLOR_MIN, variable=self.white, command=self.forward_all_values)
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
        self.labelWhite = ttk.Label(self.frame9960, text="C")
        self.labelProx = ttk.Label(self.frame9960, text="P")

        # Create flex resistor I/O
        self.sliderFlex1 = ttk.Scale(self.frameFlex, orient=tk.VERTICAL, length=200, from_=self.FLEX_MAX, to=self.FLEX_MIN, variable=self.flex1, command=self.forward_all_values)
        self.sliderFlex2 = ttk.Scale(self.frameFlex, orient=tk.VERTICAL, length=200, from_=self.FLEX_MAX, to=self.FLEX_MIN, variable=self.flex2, command=self.forward_all_values)
        self.sliderFlex3 = ttk.Scale(self.frameFlex, orient=tk.VERTICAL, length=200, from_=self.FLEX_MAX, to=self.FLEX_MIN, variable=self.flex3, command=self.forward_all_values)
        self.sliderFlex4 = ttk.Scale(self.frameFlex, orient=tk.VERTICAL, length=200, from_=self.FLEX_MAX, to=self.FLEX_MIN, variable=self.flex4, command=self.forward_all_values)
        self.labelFlex = ttk.Label(self.frameLabelFlex, text="Flex Resistors")

        # Set up our frame sizes
        self.content.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frameHeader.grid(column=0, row=0, columnspan=5, rowspan=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frame9960.grid(column=4, row=0, columnspan=2, rowspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frameFlex.grid(column=0, row=1, columnspan=5, rowspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frameLabelFlex.grid(column=0, row=1, columnspan=4, rowspan=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Position mode I/O in header frame
        self.mode1.grid(column=0, row=0)
        self.mode2.grid(column=1, row=0)
        self.mode3.grid(column=2, row=0)
        self.volume.grid(column=3, row=0)
        self.label_volume.grid(column=3, row=1)
        self.labelMode.grid(column=1, row=1)

        # Position APDS9960 I/O in header frame
        self.sliderRed.grid(column=0, row=0)
        self.sliderGreen.grid(column=1, row=0)
        self.sliderBlue.grid(column=2, row=0)
        self.sliderWhite.grid(column=3, row=0)
        self.sliderProx.grid(column=4, row=0)
        self.labelRed.grid(column=0, row=1)
        self.labelGreen.grid(column=1, row=1)
        self.labelBlue.grid(column=2, row=1)
        self.labelWhite.grid(column=3, row=1)
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

        self.tkRoot.mainloop()

    # Utility Methods - read, send, process, etc.

    def apds_light_to_midi(self, apds_reading):
        """
        Takes APDS reading as argument \n
        Returns int between 20 and 108 \n
        Convert APDS values to MIDI \n
        Floor: 20, Ceiling: 108 \n
        APDS_COLOR_MIN -> 20, APDS_COLOR_MAX -> 108
        """
        return int(apds_reading * 88 / self.APDS_COLOR_MAX) + 20
    
    def midi_to_pitch_class(self, apds_as_midi):
        """
        Takes MIDI number as argument \n
        Returns pitch class, an int between 0 and 11 \n
        Set theory represents pitches on a \n
        scale 0-11 where C = 0 regardless of octave
        """
        return int(apds_as_midi % 12)
    
    def invert_pitch_class(self, apds_as_pitch_class):
        """
        Takes pitch class as argument \n
        Returns pitch class inverted around axis \n
        apds_as_pitch_class should be a number 0-11
        """
        return (12 - apds_as_pitch_class) % 12
    
    def find_interval_class(self, pitch_class_a, pitch_class_b):
        """
        Takes two pitch classes as an argument \n
        Returns interval class, int 0 - 6 \n
        In set theory, there are only 6 possible intervals \n
        Seven intervals if you count no interval as an interval
        """
        return min((pitch_class_b - pitch_class_a) % 12, (pitch_class_a - pitch_class_b) % 12)
    
    def invert_midi(self, midi_value):
        """inverts MIDI in the spirit of set theory; 40 -> 88, 20 -> 108"""
        return 128 - midi_value
    
    def apds_light_to_low_freq(self, apds_reading):
        """
        Convert APDS values to LFO values \n
        Floor: 1, Ceiling: 20
        
        """
        return int(apds_reading * 19 / self.APDS_COLOR_MAX) + 1

    def name_greatest_color(self, index):
        match index:
            case 0:
                return "red"
            case 1:
                return "green"
            case 2:
                return "blue"
            
    def read_values(self, _=None):
        """
        read all values and return a dictionary \n
        use --prv when starting program to print well-formatted information
        """

        # I think one of the tkinter components has some implicit parameter,
        # which is why i need to do this defaulting _=None thing in the arguments

        # mode and volume
        mode_value = self.mode.get()
        volume_value = self.volume.get()

        # APDS 
        red_value = self.sliderRed.get()
        blue_value = self.sliderBlue.get()
        green_value = self.sliderGreen.get()
        white_value = self.sliderWhite.get()
        proximity_value = self.prox.get()

        # flex values
        flex_one = self.flex1.get()
        flex_two = self.flex2.get()
        flex_three = self.flex3.get()
        flex_four = self.flex4.get()

        
        # print formatted vals when flag is set
        if self.print_read_values:
            print("\n" + "="*50)
            print("CURRENT DRONE MODE VALUES:")
            print("="*50)
            
            print("\n--- Mode Settings ---")
            print(f"Mode:           {mode_value} (Mode {'I' if mode_value == 1 else 'II' if mode_value == 2 else 'III'})")
            print(f"Volume:         {volume_value} dB")
            
            print("\n--- APDS9960 Sensor Values ---")
            print(f"Red:            {red_value:,}")
            print(f"Green:          {green_value:,}")
            print(f"Blue:           {blue_value:,}")
            print(f"white:          {white_value:,}")
            print(f"Proximity:      {proximity_value}")
            
            print("\n--- Flex Resistor Values ---")
            print(f"Flex 1:         {flex_one:,}")
            print(f"Flex 2:         {flex_two:,}")
            print(f"Flex 3:         {flex_three:,}")
            print(f"Flex 4:         {flex_four:,}")
            print("="*50)

        return {
            "mode": mode_value,
            "volume": volume_value,
            "apds": {
                "red": red_value,
                "green": green_value,
                "blue": blue_value,
                "white": white_value,
                "proximity": proximity_value
            },
            "flex": {
                "flex_one": flex_one,
                "flex_two": flex_two,
                "flex_three": flex_three,
                "flex_four": flex_four,
            }

        }


    def forward_all_values(self, _=None):
        """
        read and send all values to SC \n
        I think one of the tkinter components has some implicit parameter, \n
        which is why i need to do this defaulting _=None thing in the arguments
        """
        current_state = self.read_values()

        ################### TO DO ###################
        # implement set theory methods to convert APDS inputs to something interesting
        # send them to super collider - set theory relationships can/should determine something about the quality of the drone
        # use flex sensor to affet drone:
        # - pressure increases spread of notes - from "chord" to "individual tones on different schedules"
        # - pressure mutes notes
        # - pressure adds modulation
        # how the fuck do i use proximity? maybe its a envelope filter + volume? the more you "press" the more you're pressing the sound back into the instrument
        # this could be a technique for bit crushing - "press" the sound and release to get something new out

        osc_message = [
            "mode", current_state["mode"],
            "volume", current_state["volume"],
            "red", self.apds_light_to_midi(current_state.get("apds").get("red")),
            "green", self.apds_light_to_midi(current_state.get("apds").get("green")),
            "blue", self.apds_light_to_midi(current_state.get("apds").get("blue")),
            "white", current_state.get("apds").get("white"),
            "proximity", current_state.get("apds").get("proximity"),
            "flex_one", current_state.get("flex").get("flex_one"),
            "flex_two", current_state.get("flex").get("flex_two"),
            "flex_three", current_state.get("flex").get("flex_three"),
            "flex_four", current_state.get("flex").get("flex_four")
        ]

        if current_state["mode"] == 1:
            self.client.send_message("/drone_mode", osc_message)

        
        # # some trivial computes before we send
        # vals_as_list = [red_value, green_value, blue_value]

        # index = 0
        # current_max_value = vals_as_list[index]
        # for i in range(1, len(vals_as_list)):
        #     if vals_as_list[i] > current_max_value:
        #         current_max_value = vals_as_list[i]
        #         index = i

        
        # greatest_color = self.name_greatest_color(index)
        # white_as_single_digit = math.floor(white_value / 10)

        # # A strategy: if drone_mode is enabled, send messages to /drone_mode OSC listener e.g. if mode.x_mode -> /x_mode elif mode.y_mode -> /y_mode
        # if self.mode == self.mode_enum.DRONE:
        #     self.client.send_message("/drone_mode", [red_value, blue_value, green_value, white_value, volume_value, is_checked, white_as_single_digit, greatest_color])

def run_gui(args):
    """Function to run the GUI for normal operation"""
    DroneMode(print_read_values=args.prv)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GUI to interface with Supercollider")
    parser.add_argument('--prv', action='store_true', help='Print all read values from inputs')
    args = parser.parse_args()
    
    run_gui(args)
#this is badass
from pythonosc import udp_client
import tkinter as tk
import math
import time

class DroneMode:
    def __init__(self):
        ## GUI
        self.root = tk.Tk()

        self.root.title("Drone Mode")

        # Title at the top
        self.title = tk.Label(self.root, text="Drone Mode", font = ("Arial", 18))
        self.title.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)

        self.check_state = tk.IntVar()
        self.check = tk.Checkbutton(self.root, text = "Motion Sensor Activated", font = ("Arial", 14), variable = self.check_state, command = self.forward_all_values)
        self.check.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 10)

        # slider frame
        self.slider_frame = tk.Frame(self.root)
        self.slider_frame.grid(row = 4, column = 0, columnspan = 2, padx = 10, pady = 10)

        # color square/labels + volume
        self.red_label = tk.Frame(self.slider_frame, bg = "red", width = 30, height = 30)
        self.red_label.grid(row = 0, column = 0, sticky = "ew")

        self.blue_label = tk.Frame(self.slider_frame, bg = "blue", width = 30, height = 30)
        self.blue_label.grid(row = 0, column = 1, sticky = "ew")

        self.green_label = tk.Frame(self.slider_frame, bg = "green", width = 30, height = 30)
        self.green_label.grid(row = 0, column = 2, sticky = "ew")

        self.clear_label = tk.Frame(self.slider_frame, bg = "white", width = 30, height = 30)
        self.clear_label.grid(row = 0, column = 3, sticky = "ew")

        self.volume = tk.Label(self.slider_frame, text="Volume", font = ("Arial", 18))
        self.volume.grid(row = 0, column = 4, sticky = "ew")



        # sliders
        self.red_slider = tk.Scale(self.slider_frame, from_ = 100, to = 0, command = self.forward_all_values)
        self.red_slider.grid(row = 1, column = 0, sticky = "ew")

        self.blue_slider = tk.Scale(self.slider_frame, from_ = 100, to = 0, command = self.forward_all_values)
        self.blue_slider.grid(row = 1, column = 1, sticky = "ew")

        self.green_slider = tk.Scale(self.slider_frame, from_ = 100, to = 0, command = self.forward_all_values)
        self.green_slider.grid(row = 1, column = 2, sticky = "ew")

        self.clear_slider = tk.Scale(self.slider_frame, from_ = 100, to = 0, command = self.forward_all_values)
        self.clear_slider.grid(row = 1, column = 3, sticky = "ew")

        self.volume_slider = tk.Scale(self.slider_frame, from_ = 6, to = -40, command = self.forward_all_values)
        self.volume_slider.grid(row = 1, column = 4, sticky = "ew")

        ## OSC
        self.client = udp_client.SimpleUDPClient("127.0.0.1", 57120)



        self.root.mainloop()

    def name_greatest_color(self, index):
        match index:
            case 0:
                return "red"
            case 1:
                return "green"
            case 2:
                return "blue"

    def forward_all_values(self, _=None):
        red_value = self.red_slider.get()
        blue_value = self.blue_slider.get()
        green_value = self.green_slider.get()
        clear_value = self.clear_slider.get()
        volume_value = self.volume_slider.get()
        is_checked = self.check_state.get() == 1

        # some computes before we send
        vals_as_list = [red_value, green_value, blue_value]

        index = 0
        current_max_value = vals_as_list[index]
        for i in range(1, len(vals_as_list)):
            if vals_as_list[i] > current_max_value:
                current_max_value = vals_as_list[i]
                index = i

        
        greatest_color = self.name_greatest_color(index)
        clear_as_single_digit = math.floor(clear_value / 10)

        self.client.send_message("/drone_mode", [red_value, blue_value, green_value, clear_value, volume_value, is_checked, clear_as_single_digit, greatest_color])



DroneMode()

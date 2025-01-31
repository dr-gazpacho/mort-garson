from pythonosc import udp_client
import tkinter as tk
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
        self.check = tk.Checkbutton(text = "Motion Sensor Activated", font = ("Arial", 14))

        # slider frame
        self.slider_frame = tk.Frame(self.root)
        self.slider_frame.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = 10)

        # color square/labels
        self.red_label = tk.Frame(self.slider_frame, bg = "red", width = 30, height = 30)
        self.red_label.grid(row = 0, column = 0, sticky = "ew")

        self.blue_label = tk.Frame(self.slider_frame, bg = "blue", width = 30, height = 30)
        self.blue_label.grid(row = 0, column = 1, sticky = "ew")

        self.green_label = tk.Frame(self.slider_frame, bg = "green", width = 30, height = 30)
        self.green_label.grid(row = 0, column = 2, sticky = "ew")

        self.clear_label = tk.Frame(self.slider_frame, bg = "white", width = 30, height = 30)
        self.clear_label.grid(row = 0, column = 3, sticky = "ew")



        # sliders
        self.red_slider = tk.Scale(self.slider_frame, from_ = 100, to = 0, command = self.print_color_state)
        self.red_slider.grid(row = 1, column = 0, sticky = "ew")

        self.blue_slider = tk.Scale(self.slider_frame, from_ = 100, to = 0, command = self.print_color_state)
        self.blue_slider.grid(row = 1, column = 1, sticky = "ew")

        self.green_slider = tk.Scale(self.slider_frame, from_ = 100, to = 0, command = self.print_color_state)
        self.green_slider.grid(row = 1, column = 2, sticky = "ew")

        self.clear_slider = tk.Scale(self.slider_frame, from_ = 100, to = 0, command = self.print_color_state)
        self.clear_slider.grid(row = 1, column = 3, sticky = "ew")

        ## OSC
        self.client = udp_client.SimpleUDPClient("127.0.0.1", 57120)



        self.root.mainloop()

    def show_check_state(self):
        if self.check_state.get() == 0:
            print("checked")
    
    def print_color_state(self, _=None):
        red_value = self.red_slider.get()
        blue_value = self.blue_slider.get()
        green_value = self.green_slider.get()
        clear_value = self.clear_slider.get()
        print(red_value, blue_value, green_value, clear_value)


DroneMode()
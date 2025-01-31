from pythonosc import udp_client
import tkinter as tk
import time

class DroneMode:
    def __init__(self):
        ## GUI
        self.root = tk.Tk()
        self.root.title("Drone Mode")

        # Title at the top
        self.title = tk.Label(self.root, text="Drone Mode", font=("Arial", 18))
        self.title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Create a frame for the sliders
        slider_frame = tk.Frame(self.root)
        slider_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Labels for sliders
        tk.Label(slider_frame, text="Red", font=("Arial", 12)).grid(row=0, column=0)
        tk.Label(slider_frame, text="Blue", font=("Arial", 12)).grid(row=0, column=1)
        tk.Label(slider_frame, text="Green", font=("Arial", 12)).grid(row=0, column=2)
        tk.Label(slider_frame, text="Clear", font=("Arial", 12)).grid(row=0, column=3)

        # Sliders
        self.red_slider = tk.Scale(slider_frame, from_=0, to=42, command=self.print_color_state)
        self.red_slider.grid(row=1, column=0, padx=10)

        self.blue_slider = tk.Scale(slider_frame, from_=0, to=42, command=self.print_color_state)
        self.blue_slider.grid(row=1, column=1, padx=10)

        self.green_slider = tk.Scale(slider_frame, from_=0, to=42, command=self.print_color_state)
        self.green_slider.grid(row=1, column=2, padx=10)

        self.clear_slider = tk.Scale(slider_frame, from_=0, to=42, command=self.print_color_state)
        self.clear_slider.grid(row=1, column=3, padx=10)

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
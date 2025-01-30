from pythonosc import udp_client
import tkinter as tk
import time

client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

class MyGUI:
    def __init__(self):
        self.root = tk.Tk()

        self.label = tk.Label(self.root, text = "Your Message", font = ("Arial", 18))
        self.label.pack(padx = 10, pady = 10)

        self.textbox = tk.Text(self.root, height = 5, font = ("Arial", 16))
        self.textbox.pack(padx = 10, pady = 10)

        self.check_state = tk.IntVar()
        self.check = tk.Checkbutton(self.root, text = "Show Messagebox", font = ("Arial", 16), variable = self.check_state)
        self.check.pack(padx = 10, pady = 10)

        self.root.mainloop()

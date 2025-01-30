from pythonosc import udp_client
import tkinter as tk
import time

client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

root = tk.Tk()
root.geometry("500x600")
root.title("drone_mode")

label = tk.Label(root, text = "Hello World!", font = ("Arial", 18))
label.pack(padx = 20, pady = 20)

root.mainloop()

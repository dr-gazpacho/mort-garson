from pythonosc import udp_client
import time

client = udp_client.SimpleUDPClient("127.0.0.1", 57120)


def freq(freq):
    client.send_message('/synth/params', [freq])

def free():
    client.send_message('/synth/free', [])
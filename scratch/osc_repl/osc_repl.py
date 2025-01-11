from pythonosc import udp_client
import time

client = udp_client.SimpleUDPClient("127.0.0.1", 57120)


def create(name, freq):
    client.send_message('/synth/create', [name, freq])

def freq(name, freq):
    client.send_message('/synth/params', [name, freq])

def free(name = False):
    if name:
        client.send_message('/synth/free', [name])
    else:
        client.send_message('/synth/freeAll', [])

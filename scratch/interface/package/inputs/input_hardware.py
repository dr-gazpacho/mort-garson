from tkinter import *
from tkinter import ttk
from package.inputs.input_base import InputBase
from package.types import InputResult

# Stub class to create hardware I/O interface
class InputHardware(InputBase):
  def __init__(self):
    # TODO: implement constructor
  
  def setup(self) -> None:
    # TODO: implement necessary hardware set up

  def poll(self) -> InputResult:
    # TODO: implement reading and return value
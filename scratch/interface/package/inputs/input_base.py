from abc import ABC, abstractmethod
from package.types import InputResult

# Abstract class to serve as contract between program and I/O interface
class InputBase(ABC):
  @abstractmethod
  def setup(self) -> None:
    pass

  @abstractmethod
  def poll(self) -> InputResult:
    pass
from gpiozero import Device, GPIODevice
from gpiozero.pins.native import NativeFactory
from time import sleep

# Force native pin factory
Device.pin_factory = NativeFactory()

class EncoderCounter:
    def __init__(self):
        print("Initializing GPIO pins...")
        # Using basic GPIODevice
        self.pin_a = GPIODevice(17)  # BCM pin 17
        self.pin_b = GPIODevice(27)  # BCM pin 27
        self.counter = 0
        self.last_a = self.pin_a.pin.state
        self.last_b = self.pin_b.pin.state
        print("Initialization complete")
    
    def update(self):
        """Update counter based on current pin states"""
        a = self.pin_a.pin.state
        b = self.pin_b.pin.state
        
        if a != self.last_a or b != self.last_b:
            if a != self.last_a:
                if b != a:
                    self.counter += 1
                else:
                    self.counter -= 1
                    
            self.last_a = a
            self.last_b = b
    
    def cleanup(self):
        """Close the GPIO pins"""
        self.pin_a.close()
        self.pin_b.close()

def main():
    try:
        encoder = EncoderCounter()
        last_value = 0
        
        print("Monitoring encoder. Press Ctrl+C to exit...")
        print(f"Initial state: A={encoder.pin_a.pin.state}, B={encoder.pin_b.pin.state}")
        
        while True:
            encoder.update()
            
            if encoder.counter != last_value:
                print(f"Position: {encoder.counter}")
                last_value = encoder.counter
            
            sleep(0.001)
            
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        encoder.cleanup()
        print("Cleanup complete")

if __name__ == "__main__":
    main()
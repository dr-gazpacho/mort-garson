from package.inputs.input_simulated import InputSimulated
from package.types import InputResult
import time

def main():
  # Keep cache of last inputs
  results_cached: InputResult = None
  
  # Instantiate input interface
  interface = InputSimulated()

  # Invoke setup method of instance
  interface.setup()

  
  while True:
    try:
      # Poll for changes to I/O
      results: InputResult = interface.poll()
      if (results != results_cached):
        # Cache changed results
        results_cached = results

        # Here we could fire off an osc message, I'm just printing the results
        print('Mode', results[0])
        print('APDS', results[1], results[2], results[3], results[4], results[5])
        print('Flex', results[6], results[7], results[8], results[9])
        print()
    
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        raise SystemExit
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
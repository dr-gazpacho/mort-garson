from pythonosc import udp_client
import time
import board
import busio
import adafruit_apds9960.apds9960
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
sensor.enable_proximity = True
sensor.enable_color = True

def main():
    # Create an OSC client
    # SuperCollider typically listens on port 57120 by default
    client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
    
    # Send a test message
    # Format: client.send_message("/address/pattern", [arguments])
    # client.send_message("/test", [440])
    
    # Keep the script running for a moment to ensure message is sent
    time.sleep(0.1)
    while(True):
        r, g, b, c = sensor.color_data
        print('Red: {0}, Green: {1}, Blue: {2}, Clear: {3}'.format(r, g, b, c))
        client.send_message("/n_set", [1001, "freq", r])
        time.sleep(0.1)
        client.send_message("/n_set", [1002, "freq", g])
        time.sleep(0.1)
        client.send_message("/n_set", [1003, "freq", b])
        time.sleep(0.1)
        client.send_message("/n_set", [1004, "freq", c])
        time.sleep(0.1)

if __name__ == "__main__":
    main()
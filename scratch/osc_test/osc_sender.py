from pythonosc import udp_client
import time

def main():
    # Create an OSC client
    # SuperCollider typically listens on port 57120 by default
    client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
    
    # Send a test message
    # Format: client.send_message("/address/pattern", [arguments])
    client.send_message("/test", [440, 123, 456, 789])
    client.send_message("/test", [880])
    
    # Keep the script running for a moment to ensure message is sent
    time.sleep(0.1)

if __name__ == "__main__":
    main()


# activate venv with: source venv/bin/activate /-->/ deactivate

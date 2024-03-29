import networkClass
import threading
import sys

# Flag to track if a message has been received
message_received = False

def receive_messages():
    global message_received
    try:
        while True:
            message = networkClass.receive_message(65434)
            message_received = True
            if message:
                # Display received message on a new line
                if message_received:
                    print()
                print(f"{message.sender}: {message.text}\nUser1: ", end='')
                message_received = False
    except KeyboardInterrupt:
        print("Disconnecting...")
        sys.exit()

def send_messages():
    global message_received
    try:
        while True:
            message = input("User1: ")
            # Clear the flag before sending a message
            message_received = False
            network.send_message(networkClass.Peer("Receiver", "127.0.0.1", 65435), "User1", message)
    except KeyboardInterrupt:
        print("Disconnecting...")
        sys.exit()

if __name__ == "__main__":
    # Create sender
    sender = networkClass.Peer("Sender", "127.0.0.1", 65435)

    # Add sender to network
    network = networkClass.Network()
    network.add_peer(sender)

    # Start threads for sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages)
    send_thread = threading.Thread(target=send_messages)

    # Set threads as daemon threads
    receive_thread.daemon = True
    send_thread.daemon = True

    receive_thread.start()
    send_thread.start()

    try:
        # Join threads to wait for their completion
        receive_thread.join()
        send_thread.join()
    except KeyboardInterrupt:
        print("Disconnecting...")
        sys.exit()

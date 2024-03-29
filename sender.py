import networkClass
import threading
import sys

def receive_messages():
    try:
        while True:
            message = networkClass.receive_message(65434)
            if message:
                print(f"\n{message.sender}: {message.text}\n", end='')
    except KeyboardInterrupt:
        print("Disconnecting...")
        sys.exit()

def send_messages():
    try:
        while True:
            message = input("User1: ")
            network.send_message(networkClass.Peer("Receiver", "127.0.0.1", 65435), message)
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

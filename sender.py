import networkClass
import threading
import sys

def receive_messages():
    try:
        while True:
            message = networkClass.receive_message(65435)
            if message:
                print(f"{message.sender}: {message.text}")
    except KeyboardInterrupt:
        print("Disconnecting...")
        sys.exit()

def send_messages():
    while True:
        message = input("Enter message to send: ")
        network.send_message(networkClass.Peer("Sender", "127.0.0.1", 65435), message)

if __name__ == "__main__":
    # Create sender
    sender = networkClass.Peer("Sender", "127.0.0.1", 65435)

    # Add sender to network
    network = networkClass.Network()
    network.add_peer(sender)

    # Start threads for sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages)
    send_thread = threading.Thread(target=send_messages)

    receive_thread.start()
    send_thread.start()

    # Join threads to wait for their completion
    receive_thread.join()
    send_thread.join()

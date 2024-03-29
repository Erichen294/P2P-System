import networkClass
import threading
import sys

def receive_messages():
    try:
        while True:
            message = networkClass.receive_message(65434)
            if message:
                print(f"{message.sender}: {message.text}")
    except KeyboardInterrupt:
        print("Disconnecting...")
        sys.exit()

def send_messages():
    while True:
        message = input("Enter message to send: ")
        network.send_message(networkClass.Peer("Receiver", "127.0.0.1", 65434), message)

if __name__ == "__main__":
    # Create receiver
    receiver = networkClass.Peer("Receiver", "127.0.0.1", 65434)

    # Add receiver to network
    network = networkClass.Network()
    network.add_peer(receiver)

    # Start threads for sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages)
    send_thread = threading.Thread(target=send_messages)

    receive_thread.start()
    send_thread.start()

    # Join threads to wait for their completion
    receive_thread.join()
    send_thread.join()

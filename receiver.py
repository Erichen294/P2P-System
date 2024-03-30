import networkClass
import threading
import sys
import os

# Flag to track if a message has been received
message_received = False

# Flag to indicate if threads should stop
stop_threads = False

def receive_messages():
    global message_received, stop_threads
    try:
        while not stop_threads:
            message = networkClass.receive_message(65435)
            message_received = True
            if message:
                # Display received message on a new line
                if message_received:
                    print()
                print(f"{message.sender}: {message.text}\nUser2: ", end='')
                message_received = False
    except KeyboardInterrupt:
        pass  # Let the thread exit gracefully without printing
    finally:
        print("Disconnecting...")
        os._exit(0)  # Exit the thread forcefully

def send_messages():
    global message_received, stop_threads
    try:
        while not stop_threads:
            message = input("User2: ")
            # Clear the flag before sending a message
            message_received = False
            network.send_message(networkClass.Peer("Receiver", "127.0.0.1", 65434), "User2", message)
    except KeyboardInterrupt:
        pass  # Let the thread exit gracefully without printing
    except EOFError:
        pass  # Let the thread exit gracefully without printing
    finally:
        print("Disconnecting...")
        os._exit(0)  # Exit the thread forcefully

if __name__ == "__main__":
    # Create sender
    receiver = networkClass.Peer("Receiver", "127.0.0.1", 65434)

    # Add sender to network
    network = networkClass.Network()
    network.add_peer(receiver)

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
        stop_threads = True  # Set the flag to stop threads
        os._exit(0)  # Exit the main thread forcefully

import networkClass
import threading
import os
import sqlite3
import time

# Flag to track if a message has been received
message_received = False

# Flag to indicate if threads should stop
stop_threads = False

# SQLite database file name
DB_FILE = "user1.db"

# Create a SQLite connection and cursor
connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

# Create the messages table if it doesn't exist
networkClass.create_database(DB_FILE)

# Function to fetch and print messages from the database if relevant
def print_previous_messages():
    messages = networkClass.get_messages(DB_FILE)
    if messages:
        print("Previous messages:")
        for sender, text in messages:
            # Check if the sender or receiver is the current conversation partner
            if sender == "User2" or sender == "User1":
                print(f"{sender}: {text}")

# Print previous messages before starting threads
print_previous_messages()

def receive_messages():
    global message_received, stop_threads
    try:
        while not stop_threads:
            message = networkClass.receive_message(65434)
            message_received = True
            if message:
                if message_received:
                    print()
                print(f"{message.sender}: {message.text}\nUser1: ", end='')
                networkClass.insert_message(message.sender, message.text, DB_FILE)
                message_received = False
    except KeyboardInterrupt:
        pass  
    finally:
        print("Disconnecting...")
        connection.close()  # Close the SQLite connection upon termination

def send_messages():
    global message_received, stop_threads
    try:
        while not stop_threads:
            message = input("User1: ")
            message_received = False
            network.send_message(networkClass.Peer("User2", "127.0.0.1", 65435), "User1", message)
            networkClass.insert_message("User1", message, DB_FILE)
    except KeyboardInterrupt:
        pass  
    except EOFError:
        pass  
    finally:
        print("Disconnecting...")
        os._exit(0) 

if __name__ == "__main__":
    # Create user1
    user1 = networkClass.Peer("User1", "127.0.0.1", 65435)

    # Add sender to network
    network = networkClass.Network()
    network.add_peer(user1)

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
        stop_threads = True  
        print("Main: Disconnecting...")  # Print a message indicating normal termination

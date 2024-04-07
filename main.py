import sqlite3
import socket
import threading
import os
import networkClass

# SQLite database file names
DB_FILE_USERS = "users.db"
DB_FILE_CONTACTS = "contacts.db"
DB_FILE_MESSAGES = "messages.db"

# Flag to track if a message has been received
message_received = False

# Flag to indicate if threads should stop
stop_threads = False

# Function to create the users table if it doesn't exist
def create_users_table():
    conn = sqlite3.connect(DB_FILE_USERS)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 username TEXT PRIMARY KEY,
                 password TEXT,
                 ip_address TEXT,
                 port INTEGER
                 )''')
    conn.commit()
    conn.close()

# Function to create the contacts table if it doesn't exist
def create_contacts_table():
    conn = sqlite3.connect(DB_FILE_CONTACTS)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
                 user TEXT,
                 contact TEXT,
                 ip_address TEXT,
                 port INTEGER,
                 PRIMARY KEY (user, contact, ip_address, port)
                 )''')
    conn.commit()
    conn.close()

# Function to register a new user
def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    ip_address = input("Enter ip address: ")

    # Fetch the last assigned port
    conn = sqlite3.connect(DB_FILE_USERS)
    c = conn.cursor()
    c.execute("SELECT MAX(port) FROM users")
    last_port = c.fetchone()[0]
    conn.close()

    if last_port is None:
        port = 65432  # Start from 65432 if no user exists yet
    else:
        port = last_port + 1  # Increment by one for each new user

    # Insert the new user along with their assigned port
    conn = sqlite3.connect(DB_FILE_USERS)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, ip_address, port) VALUES (?, ?, ?, ?)", (username, password, ip_address, port))
    conn.commit()
    conn.close()
    
    print("Registration successful!")

# Function to log in an existing user
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    conn = sqlite3.connect(DB_FILE_USERS)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    
    if user:
        print("Login successful!")
        return user
    else:
        print("Invalid username or password.")
        return None

# Function to view contacts list
def view_contacts(username):
    conn = sqlite3.connect(DB_FILE_CONTACTS)
    c = conn.cursor()
    c.execute("SELECT * FROM contacts WHERE user=?", (username,))
    contacts = c.fetchall()
    conn.close()
    
    if contacts:
        print("Your Contacts:")
        for contact in contacts:
            print(f"Username: {contact[1]}, IP Address: {contact[2]}, Port: {contact[3]}")
    else:
        print("Your contacts list is empty.")

# Function to add a contact
def add_contact(username):
    contact = input("Enter contact name: ")
    ip_address = input("Enter IP Address: ")
    port = int(input("Enter Port: "))
    
    conn = sqlite3.connect(DB_FILE_CONTACTS)
    c = conn.cursor()
    c.execute("INSERT INTO contacts (user, contact, ip_address, port) VALUES (?, ?, ?, ?)", (username, contact, ip_address, port))
    conn.commit()
    conn.close()
    
    print("Contact added successfully.")

# Function to connect to a contact
def connect_to_contact(user, contact):
    # Query the database to check if the contact exists in the user's contacts list
    conn = sqlite3.connect(DB_FILE_CONTACTS)
    c = conn.cursor()
    c.execute("SELECT ip_address, port FROM contacts WHERE user=? AND contact=?", (user, contact))
    contact_info = c.fetchone()
    conn.close()

    if contact_info:
        ip_address, port = contact_info

        # Attempt connection
        try:
            # Create a socket object
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set a timeout for the connection attempt
            client_socket.settimeout(5)
            # Connect to the contact's IP address and port
            client_socket.connect((ip_address, port))
            # If connection succeeds, return True
            print("Connection successful!")
            return 0, ip_address, port
        except Exception as e:
            # If connection fails, print error message and return False
            print(f"Connection failed: {e}")
            return 1, ip_address, port
    else:
        print("Contact not found in your contacts list.")
        return -1, None, None
    
# Function to start the user as a server
def start_server(username):
    # Query the user database for the current user's IP address and port
    conn = sqlite3.connect(DB_FILE_USERS)
    c = conn.cursor()
    c.execute("SELECT ip_address, port FROM users WHERE username=?", (username,))
    user_info = c.fetchone()
    conn.close()
     
    if user_info:
        ip_address, port = user_info

        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Bind the socket to the user's IP address and port
            server_socket.bind((ip_address, port))
            print(f"Server started on {ip_address}:{port}")

            # Listen for incoming connections
            server_socket.listen()

            while True:
                # Accept a new connection
                client_socket, client_address = server_socket.accept()
                print(f"Connection established with {client_address}")

                # Start a new thread or process to handle the client connection
                handle_client_thread = threading.Thread(target=handle_client, args=(client_socket, username))
                handle_client_thread.start()

        except Exception as e:
            print(f"Error starting server: {e}")

    else:
        print("User not found.")

def handle_client(client_socket, username):
    """
    Function to handle client connection.
    You can implement your handling logic here.
    """
    try:
        while True:
            # Receive message from the client
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"Received message from client: {message}")

                # Extract client's IP address and port from the message
                client_ip, client_port, sender_username, client_message = message.split(':')

                # Process the received message if needed
                server_message = input(f"{username}: ")
                client_socket.sendto(server_message.encode("utf-8"), (client_ip, int(client_port)))
    except ConnectionResetError:
        print("Connection with client closed.")
        client_socket.close()

def send_messages(username, contact_name, contact_ip, contact_port, client_ip, client_port):
    global message_received, stop_threads
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
         # Connect to the contact's IP address and port
        client_socket.connect((contact_ip, contact_port))

        while not stop_threads:
            # Get message input from user
            message = input(f"{username}: ")
            message_received = False
            
            full_message = f"{client_ip}:{client_port}:{username}: {message}"

            # Send the message
            client_socket.sendall(full_message.encode('utf-8'))
            
            # Insert message into the database
            networkClass.insert_message(username, contact_name, message, DB_FILE_MESSAGES)
            
    except KeyboardInterrupt:
        print("Disconnecting...")
        client_socket.close()
        os._exit(0)   
    except EOFError:
        print("Disconnecting...")
        client_socket.close()
        os._exit(0)   

def receive_messages(username, client_ip, client_port):
    global message_received, stop_threads
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((client_ip, client_port))

        while not stop_threads:
            message, _ = client_socket.recvfrom(1024)
            message = message.decode("utf-8")
            if message:
                print(f"{message}\n{username}: ", end='')
    except KeyboardInterrupt:
        print("Disconnecting...")
        client_socket.close()
        os._exit(0)   

def get_user_info(username):
    conn = sqlite3.connect(DB_FILE_USERS)
    c = conn.cursor()
    c.execute("SELECT ip_address, port FROM users WHERE username=?", (username,))
    user_info = c.fetchone()
    conn.close()

    return user_info

def main():
    create_users_table()
    create_contacts_table()
    networkClass.create_database(DB_FILE_MESSAGES)

    while True:
        print("1. Register")
        print("2. Log in")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                while True:
                    print("1. View contacts")
                    print("2. Add contact")
                    print("3. Connect to user")
                    print("4. Set up as server")
                    print("5. Log out")
                    inner_choice = input("Enter your choice: ")
                    if inner_choice == "1":
                        view_contacts(user[0])
                    elif inner_choice == "2":
                        add_contact(user[0])
                    elif inner_choice == "3":
                        contact = input("Enter the contact name: ")
                        connect, ip_address, port = connect_to_contact(user[0], contact)
                        if connect == 0:
                            # Connection succeeded
                            client = networkClass.Peer(user[0], user[2], user[3])
                            network = networkClass.Network()
                            network.add_peer(client)

                            # Get client ip and port
                            client_ip, client_port = get_user_info(user[0])

                            # Start threads for sending and receiving messages
                            receive_thread = threading.Thread(target=receive_messages, args=(user[0], client_ip, client_port))
                            send_thread = threading.Thread(target=send_messages, args=(user[0], contact, ip_address, port, client_ip, client_port))

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
                    elif inner_choice == "4":
                        start_server(user[0])
                    elif inner_choice == "5":
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 5.")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

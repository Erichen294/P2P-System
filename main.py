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

def fetch_chat_history(sender, receiver, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM messages WHERE (sender=? OR receiver=?) OR (sender=? OR receiver=?)", (sender, receiver, receiver, sender))
    messages = c.fetchall()
    conn.close()

    if messages:
        print("Previous messages:")
        for user1, user2, message in messages:
                print(f"{user1}: {message}")


def create_user_database(username):
    db_file = f"{username}.db"
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS messages (
                     sender TEXT,
                     receiver TEXT,
                     message TEXT
                     )''')
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        conn.commit()
        conn.close()

# Function to start the user as a server
def start_server(server_name):
    # Query the user database for the current user's IP address and port
    conn = sqlite3.connect(DB_FILE_USERS)
    c = conn.cursor()
    c.execute("SELECT ip_address, port FROM users WHERE username=?", (server_name,))
    user_info = c.fetchone()
    conn.close()
     
    if user_info:
        ip_address, port = user_info

        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip_address, port))
        server_socket.listen()
        print(f"Server started on {ip_address}:{port}")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Connection established with {client_address}")

                # Start a new thread to handle each client connection
                client_thread = threading.Thread(target=handle_client, args=(server_name, client_socket))
                client_thread.start()
        except KeyboardInterrupt:
            print("\nExiting server...")

    else:
        print("User not found.")

def handle_client(server_name, client_socket):
    """
    Function to handle client connection.
    You can implement your handling logic here.
    """
    printHistory = True
    try:
        while True:
            # Receive message from the client
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break  # If the client closes the connection, exit the loop

            client, _, message = message.partition(':')
            if printHistory:
                printHistory = False
                fetch_chat_history(client, server_name, f"{server_name}.db")
            networkClass.insert_message(client, server_name, message.lstrip(), f"{server_name}.db")
            print(f"{client}:{message}")

            # Send a response back to the client
            response = input(f"{server_name}: ")
            networkClass.insert_message(server_name, client, response, f"{server_name}.db")
            response = f"{server_name}:{response}"
            client_socket.sendall(response.encode("utf-8"))

    except KeyboardInterrupt:
        print("Exiting server...")
        client_socket.close()
  
def send_message(client, server_name, client_socket):
    try:
        while True:
            # Get message input from user
            message = input(f"{client}: ")
            networkClass.insert_message(client, server_name, message, f"{client}.db")
            message = f"{client}: {message}"

            # Send the message to the server
            client_socket.sendall(message.encode("utf-8"))
            
            # Receive response from the server
            response = client_socket.recv(1024).decode("utf-8")
            server, _, message = response.partition(':')
            networkClass.insert_message(server_name, client, message, f"{client}.db")
            print(f"{server}: {message}")

    except KeyboardInterrupt:
        print("Disconnecting...")
        client_socket.close()
        os._exit(0)
    
def start_client(client, server_name, server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    print(f"Connected to server {server_ip}:{server_port}")

    fetch_chat_history(client, server_name, f"{client}.db")

    # Start a thread to send messages
    send_thread = threading.Thread(target=send_message, args=(client, server_name, client_socket))
    send_thread.start()

    try:
        send_thread.join()
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

    while True:
        print("1. Register")
        print("2. Log in")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            create_user_database(user[0])
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
                            start_client(user[0], contact, ip_address, port)
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

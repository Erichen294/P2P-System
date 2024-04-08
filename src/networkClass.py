import socket
import sqlite3

def create_database(name):
    conn = sqlite3.connect(name)
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

def insert_message(sender, receiver, message, name):
    conn = sqlite3.connect(name)
    c = conn.cursor()
    c.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)", (sender, receiver, message))
    conn.commit()
    conn.close()

def get_messages(name):
    conn = sqlite3.connect(name)
    c = conn.cursor()
    c.execute("SELECT sender_username, message FROM messages")
    messages = c.fetchall()
    conn.close()
    return messages

class Message:
    def __init__(self, sender, text):
        self.sender = sender
        self.text = text

def receive_message(sender_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', sender_port))  # Bind to the sender's port
        server_socket.listen()

        # Accept incoming connection
        conn, addr = server_socket.accept()
        with conn:
            # Receive data from the connected client
            data = conn.recv(1024).decode('utf-8')

            # Split the received data into sender's username and message content
            sender_username, message_text = data.split(':', 1)

            # Return a Message object containing the sender and message content
            return Message(sender_username.strip(), message_text.strip())

        
class Peer:
    def __init__(self, username, ip_address, port):
        self.username = username
        self.ip_address = ip_address
        self.port = port

class Network:
    def __init__(self):
        self.peers = []

    def broadcast(self, message):
        for peer in self.peers:
            self.send_message(peer, message)

    def send_message(self, peer, sender_username, message):
        # Concatenate sender's username with the message
        message = f"{sender_username}: {message}"

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((peer.ip_address, peer.port))
            client_socket.sendall(message.encode('utf-8'))

    def add_peer(self, peer):
        self.peers.append(peer)

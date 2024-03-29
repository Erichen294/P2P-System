import socket

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
            data = conn.recv(1024)

            # Return a Message object containing the sender and message content
            return Message(addr[1], data.decode('utf-8'))

        
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

    def send_message(self, peer, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((peer.ip_address, peer.port))
            client_socket.sendall(message.encode('utf-8'))

    def add_peer(self, peer):
        self.peers.append(peer)
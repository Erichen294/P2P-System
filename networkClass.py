import socket

def receive_message(sender_ip):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((sender_ip, 65433))  # Bind to all available interfaces and the specified port
        server_socket.listen()

        print("Waiting for incoming messages...")

        # Accept incoming connection
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")

            # Receive data from the connected client
            data = conn.recv(1024)

            # Return the received data (message)
            return data.decode('utf-8')
        
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
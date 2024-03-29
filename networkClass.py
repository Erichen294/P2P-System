import socket

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
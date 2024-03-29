import networkClass

if __name__ == "__main__":
    # Creating first peer
    eric = networkClass.Peer("Eric", "10.239.90.181", 65432)

    # Adding peer to network
    network = networkClass.Network()
    network.add_peer(eric)

    # Sending message
    network.send_message(networkClass.Peer("Bob", "10.239.252.154", 65433), "Hello from Eric!")
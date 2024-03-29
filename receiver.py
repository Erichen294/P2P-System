import networkClass

if __name__ == "__main__":
    # Creating Bob
    bob = networkClass.Peer("Bob", "10.239.252.154", 65433)

    # Adding peer to network
    network = networkClass.Network()
    network.add_peer(bob)

    # Receiving message
    while True:
        message = networkClass.receive_message("10.239.90.181")
        if message:
            print(f"Received message: {message}")
            break 
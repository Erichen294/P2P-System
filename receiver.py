import networkClass

if __name__ == "__main__":
    # Creating Bob
    receiver = networkClass.Peer("Receiver", "127.0.0.1", 65434)

    # Adding peer to network
    network = networkClass.Network()
    network.add_peer(receiver)

    # Receiving message
    while True:
        message = networkClass.receive_message()
        if message:
            print(f"Received message: {message}")
            break 
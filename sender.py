import networkClass

if __name__ == "__main__":
    # Creating sender
    sender = networkClass.Peer("Sender", "127.0.0.1", 65434)

    # Adding peer to network
    network = networkClass.Network()
    network.add_peer(sender)

    # Sending message
    network.send_message(networkClass.Peer("Receiver", "127.0.0.1", 65434), "Hello from Sender!")
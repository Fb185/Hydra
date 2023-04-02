# Documentation: Node-Based Application

This script implements a simple node-based  application using a peer-to-peer network architecture. Each node in the network communicates with its peers using sockets and threads to send and receive messages. The network is decentralized, meaning there is no central server to manage connections or relay messages.

## Network Architecture

The network architecture used in this application is a **peer-to-peer (P2P)** architecture. Each participant in the network, referred to as a "node," can connect to any other node in the network, send messages, and receive messages from its peers. Unlike client-server architectures, there is no central authority that manages connections or routes messages. The P2P architecture is highly distributed and allows for the network to continue functioning even if some nodes are disconnected.

## Class: Node

The `Node` class defines the structure and behavior of a node in the network. It has the following methods:

### `__init__(self, port)`

This constructor initializes a node with the given port. It sets up a server socket to listen for incoming connections from other nodes.

### `handle_peer(self, client_socket)`

This method handles incoming messages from a connected peer. It receives messages, decodes them, and prints them to the console. If an error occurs or the connection is closed, it will break the loop and close the client socket.

### `send_message(self, msg)`

This method sends a message to all connected peers. It iterates through the list of peers, creates a new socket for each one, and sends the message. If an error occurs during the process, it will continue to the next peer.

### `listen(self)`

This method listens for incoming connections and messages from other nodes. It sets a timeout of 1 second for the server socket to prevent blocking. When a new connection is accepted, it reads the header and data from the incoming message. If the header is 'P:', it adds the peer to its list and starts a new thread to handle the peer. If the header is 'M:', it prints the received message.

### `connect_to_peers(self)`

This method tries to connect to other nodes in the network with port numbers ranging from 8000 to the current node's port number. If a connection is successful, it sends the current node's port to the peer, adds the peer to the list of peers, and starts a new thread to handle the peer.

## Function: main()

The `main()` function is the entry point of the application. It initializes a new node, connects to existing peers, sends a connection message to the network, and starts a thread to listen for incoming messages. It then enters an input loop that allows the user to send messages or exit the application. When the user exits, the node sends a disconnection message to the network, sets the `closed` flag, and closes the server socket before exiting the application.

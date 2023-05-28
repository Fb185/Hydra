import socket
import threading
import random

class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []
        self.server_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Maximum number of queued connections

        print(f"Node listening at {self.host}:{self.port}")

        threading.Thread(target=self.accept_connections).start()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.peers.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print("\nReceived message:", message)
                    self.forward_message(message, client_socket)
                else:
                    self.peers.remove(client_socket)
                    client_socket.close()
                    break
            except Exception as e:
                self.peers.remove(client_socket)
                client_socket.close()
                break

    def forward_message(self, message, sender_socket):
        for client_socket in self.peers:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except Exception as e:
                    print("Failed to forward message:", e)

    def send_message(self, message):
        for client_socket in self.peers:
            try:
                client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print("Failed to send message:", e)

    def close(self):
        self.server_socket.close()
        for client_socket in self.peers:
            client_socket.close()

if __name__ == '__main__':
    host = "127.0.0.1"
    port = random.randint(1024, 65535)
    node = Node(host, port)

    try:
        node.start()

        while True:
            message = input("Enter message: ")
            node.send_message(message)

    except KeyboardInterrupt:
        node.close()

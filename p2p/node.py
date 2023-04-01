import socket
import threading
import sys
# import time

class Node:
    def __init__(self, port):
        self.port = port
        self.peers = []
        self.closed = False
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('127.0.0.1', self.port))



    def handle_peer(self, client_socket):
        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                print(msg)
            except Exception as e:
                break
        client_socket.close()

    def send_message(self, msg):
        for peer in self.peers:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', peer))
                s.send(f'M:{msg}'.encode('utf-8'))
                s.close()
            except Exception as e:
                pass

    # def listen(self):
    #     self.server_socket.listen()
    #     while self.running:
    #         try:
    #             self.server_socket.settimeout(1)
    #             client_socket, addr = self.server_socket.accept()
    #             header = client_socket.recv(2).decode('utf-8')
    #             data = client_socket.recv(1024).decode('utf-8')

    #             if header == 'P:':
    #                 if not data:
    #                     continue
    #                 self.peers.append(int(data))
    #                 threading.Thread(target=self.handle_peer, args=(client_socket,)).start()
    #             elif header == 'M:':
    #                 print(f'\n{data}')
    #         except socket.timeout:
    #             pass
    def listen(self):
        self.server_socket.listen()
        self.server_socket.settimeout(1)  # Set a timeout of 1 second
        while not self.closed:
            try:
                client_socket, addr = self.server_socket.accept()
                header = client_socket.recv(2).decode('utf-8')
                data = client_socket.recv(1024).decode('utf-8')

                if header == 'P:':
                    if not data:
                        continue
                    self.peers.append(int(data))
                    threading.Thread(target=self.handle_peer, args=(client_socket,)).start()
                elif header == 'M:':
                    print(f'\n{data}')
            except socket.timeout:
                continue  # If the timeout occurs, just continue the loop
            except OSError as e:
                break  # If the server socket is closed, break the loop

    def connect_to_peers(self):
        for i in range(8000, self.port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', i))
                s.send(f'P:{self.port}'.encode('utf-8'))
                self.peers.append(i)
                threading.Thread(target=self.handle_peer, args=(s,)).start()
            except Exception as e:
                pass

def main():
    port = 8000
    while True:
        try:
            node = Node(port)
            break
        except Exception as e:
            port += 1

    print(f"Node started on port {port}")
    node.connect_to_peers()
    node.send_message(f"\nNode {port} has connected to the network")

    threading.Thread(target=node.listen).start()

    while True:
        command = input("Enter command (send/exit): ")
        if command == "send":
            msg = input("Enter message: ")
            node.send_message(f"\nNode {port}: {msg}")
        elif command == "exit":
            node.send_message(f"Node {port} has disconnected from the network")
            node.closed = True
            node.server_socket.close()
            sys.exit()

if __name__ == "__main__":
    main()

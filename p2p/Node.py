import socket
import threading
import sys
from Task import Task

class Node():
    def __init__(self, port):
        self.port = port
        self.peers = []
        self.closed = False
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('127.0.0.1', self.port))
        self.accepted_tasks = []
        self.available_tasks = []

    def send_to_all_peers(self, msg):
        for peer in self.peers:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', peer))
                s.send(msg.encode('utf-8'))
                threading.Thread(target=self.handle_peer, args=(s,)).start()
                s.close()
            except Exception as e:
                pass

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
                # s.close()
            except Exception as e:
                pass

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
                    for task in self.available_tasks:
                        task_str = f"{task.id}:{task.description}:{task.author}:{','.join(str(node) for node in task.accepted_nodes)}:{task.complete}:{task.full}"
                        client_socket.send(f'T:{task_str}'.encode('utf-8'))
                elif header == 'M:':
                    print(f'\n{data}')

                elif header == 'T:':
                    task_obj = Task.from_string(data)
                    self.available_tasks.append(task_obj)

                elif header == 'A:':
                    # self.accept_task.append(data)
                    self.accept_task(data)

                elif header == 'S:':
                    self.syncronize(data)

            except socket.timeout:
                continue  # If the timeout occurs, just continue the loop
            except OSError as e:
                break  # If the server socket is closed, break the loop

    def connect_to_peers(self):
        for i in range(8000, self.port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1/2)  # Add a timeout to the socket
                s.connect(('127.0.0.1', i))
                s.send(f'P:{self.port}'.encode('utf-8'))
                self.peers.append(i)
                threading.Thread(target=self.handle_peer, args=(s,)).start()

                while True:  # Receive tasks from the connected peer
                    try:
                        header = s.recv(2).decode('utf-8')
                        if not header:
                            break

                        if header == 'T:':
                            data = s.recv(1024).decode('utf-8')
                            received_task = Task.from_string(data)
                            if not self.task_exists(received_task.id):
                                self.available_tasks.append(received_task)
                    except socket.timeout:
                        break  # Break the loop when the timeout occurs

            except Exception as e:
                pass

    def task_exists(self, task_id):
        for task in self.available_tasks:
            print(task)
            if task.id == int(task_id):
                return True
        return False


    def make_task(self, description, task_id):
        print("checking dupes")
        # print(task_id)
        if self.task_exists(task_id):
            print("Duplicate ID")
            return None

        new_task = Task(description, self.port, task_id)
        self.available_tasks.append(new_task)

        for peer in self.peers:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', peer))
                self.send_message(f"\nNew task by {self.port}")
                self.send_message(f"\nTask{new_task.id}: {new_task.description}")
                task_str = f"{new_task.id}:{new_task.description}:{new_task.author}:{','.join(str(node) for node in new_task.accepted_nodes)}:{new_task.complete}:{new_task.full}"
                s.send(f'T:{task_str}'.encode('utf-8'))
                s.close()
            except Exception as e:
                pass
        print(self.available_tasks)
        return None


    def is_full_task(self, task_id) -> None:
        # print(self.available_tasks[int(task_id) -1].accepted_nodes)
        if len(self.available_tasks[int(task_id) -1].accepted_nodes) == 2:
            print("Task full")
            return

    def accept_task(self, task_id):

        self.is_full_task(task_id)

        if not self.task_exists(task_id):
            print("Task not found")
            return

        for peer in self.peers:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', peer))
                self.available_tasks[int(task_id)-1]
                s.send(f'S:{self.port}:{task_id}'.encode('utf-8')) # send syncronize
                self.send_message(f'{self.port} has accepted task {task_id}')
            except Exception as e:
                pass

        if self.available_tasks[int(task_id)-1].accepted_nodes[0] == None:
            self.available_tasks[int(task_id)-1].accepted_nodes[0] = self.port
        else:
            self.available_tasks[int(task_id)-1].accepted_nodes[1] = self.port
        self.accepted_tasks.append(self.available_tasks[int(task_id)-1])
        self.available_tasks.pop(int(task_id)-1)

    def syncronize(self, data):
        print("\nSyncronizing...")
        data = data.split(":")
        port = data[0]
        task_id = int(data[1])
        # print(self.available_tasks[0].accepted_nodes[0])


        for task in self.available_tasks:
            if task.id == int(task_id):
                print("aN0 ", task.accepted_nodes[0])
                if task.accepted_nodes[0] == None:
                    task.accepted_nodes[0] = int(port)
                else:
                    task.accepted_nodes[1] = int(port)
            else:
                print("\nfuck")

        for task in self.accepted_tasks:
            if task.id == int(task_id):
                if task.accepted_nodes[0] == None:
                    task.accepted_nodes[0] = int(port)
                else:
                    task.accepted_nodes[1] = int(port)

    def list_available_tasks(self):
        for task in self.available_tasks:
            print(str(task))

    def list_accepted_tasks(self):
        for task in self.accepted_tasks:
            print(str(task))


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
        command = input("Enter command (send/exit/make/list(a)/accept): ")
        if command == "send":
            msg = input("Enter message: ")
            node.send_message(f"\nNode {port}: {msg}")

        elif command == "make":
            descriprion = input("Enter a description ")
            task_id = input("Enter a task ID ")
            node.make_task(descriprion, task_id)

        elif command == "list":
            node.list_available_tasks()

        elif command == "lista":
            node.list_accepted_tasks()

        elif command == "accept":
            task_id = input("Enter a task ID ")
            node.accept_task(task_id)

        elif command == "exit":
            node.send_message(f"Node {port} has disconnected from the network")
            node.closed = True
            node.server_socket.close()
            sys.exit()


if __name__ == "__main__":
    main()

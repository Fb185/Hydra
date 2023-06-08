import socket
import threading
import sys
from Task import Task
import random

class Node():
    def __init__(self, port):
        self.port = port
        self.peers = []
        self.closed = False
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        self.server_socket.bind(('127.0.0.1', self.port))
        self.given_tasks = []
        self.my_tasks = []
        self.global_task_id = 0
        self.balance = 10
        self.stake = 0
        

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
                s.close()
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
                    for task in Task.task_history:
                        task_str = f"{task.id}:{task.description}:{task.author}:{','.join(str(node) for node in task.given_tasks)}:{task.complete}"
                        client_socket.send(f'T:{task_str}'.encode('utf-8'))
                elif header == 'M:':
                    print(f'\n{data}')

                elif header == 'i:':
                    self.global_task_id = int(data)

                elif header == 'T:':
                    task_obj = Task.from_string(data)
                    self.given_tasks.append(task_obj)

                elif header == 'A:':
                    self.accept_task(data)

                elif header == 'S:':
                    self.syncronize_tasks(data)

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
                                self.given_tasks.append(received_task)
                    except socket.timeout:
                        break  # Break the loop when the timeout occurs
            except Exception as e:
                pass

    def task_exists(self, task_id):
        for task in self.given_tasks:
            if task.id == task_id:
                return True

        for task in self.task_history:
            if task.id == task_id:
                return True

        return False

    def make_task(self, description):
        assigned_n = random.sample(set(self.peers) - {self.port}, k=4)
        new_task = Task(description, self.port, assigned_n, self.global_task_id)
        self.global_task_id += 1

        new_task.assigned_nodes = assigned_n
        self.my_tasks.append(new_task)
        Task().task_history.append(new_task)
        # Send the task information to the assigned nodes
        for peer in assigned_n:
            try:
                self.given_tasks.append(new_task)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                s.connect(('127.0.0.1', peer))
                task_str = f"{new_task.id}:{new_task.description}:{new_task.author}:{','.join(str(node) for node in new_task.accepted_nodes)}:{new_task.complete}"
                s.send(f'T:{task_str}'.encode('utf-8'))
                s.send(f'i:{self.global_task_id}'.encode('utf-8'))
                s.send(f'A:{new_task.id}'.encode('utf-8'))  # Add task ID to accepted tasks of assigned nodes
                message = f"You have been assigned task {new_task.id}."
                s.send(f'M:{message}'.encode('utf-8'))
                s.close()
            except Exception as e:
                pass

    def syncronize_tasks(self, data):
        print("\nSynchronizing...")
        data = data.split(":")
        port = data[0]
        task_id = int(data[1])

        for task in self.task_history:
            if task.id == int(task_id):
                if task.assigned_nodes[0] is None:
                    task.assigned_nodes[0] = int(port)
                else:
                    task.assigned_nodes[1] = int(port)

    def notify_assigned_nodes(self, assigned_nodes, task):
        message = f'Assigned task {task.id} - {task.description}'
        for node in assigned_nodes:
            node.send_message(message)

    def add_given_task(self, task):
        self.given_tasks.append(task)

    def list_given_tasks(self):
        for task in self.given_tasks:
            print(str(task))

    def list_my_tasks(self):
        for task in self.my_tasks:
            print(str(task))
    """
    def accept_task(self, data):
        print(f"\nTask {data} accepted by {self.port}")
        task_id = int(data)
        for task in self.task_history:
            if task.id == task_id:
                task.assigned_nodes.append(self.port)
                break
        """
    def get_balance(self):
        print(f"\nYour balance is - {self.balance}")

    def get_stake(self):
        print(f"\nYour stake is - {self.stake}")

    def add_balance(self, amount):
        self.balance += amount
        print(f"\nBalance of {self.port} updated to {self.balance}")

    def add_Stake(self, amount):
        self.stake += amount

    def exit(self):
        print(f"\nNode {self.port} exited")
        self.closed = True
        self.server_socket.close()
        sys.exit()

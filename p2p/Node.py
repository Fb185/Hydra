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
        self.history_tasks = []
        self.my_tasks = []
        self.global_task_id = 0

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
                        task_str = f"{task.id}:{task.description}:{task.author}:{','.join(str(node) for node in task.accepted_nodes)}:{task.complete}"
                        client_socket.send(f'T:{task_str}'.encode('utf-8'))
                elif header == 'M:':
                    print(f'\n{data}')

                elif header == 'i:':
                    self.global_task_id = int(data)

                elif header == 'T:':
                    task_obj = Task.from_string(data)
                    self.available_tasks.append(task_obj)
                    self.history_tasks.append(task_obj)

                elif header == 'A:':
                    # self.accept_task.append(data)
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
                                self.available_tasks.append(received_task)
                    except socket.timeout:
                        break  # Break the loop when the timeout occurs

            except Exception as e:
                pass

    def task_exists(self, task_id):
        for task in self.available_tasks:
            if task.id == int(task_id):
                return True

        for task in self.accepted_tasks:
            if task.id == int(task_id):
                return True
        return False



    def make_task(self, description):
        print("checking dupes")
        # print(task_id)
        # if self.task_exists(task_id):
        #     print("Duplicate ID\n Unable to create task.")
        #     return None

        new_task = Task(description, self.port, self.global_task_id)
        self.global_task_id+=1

        self.available_tasks.append(new_task)
        self.history_tasks.append(new_task)
        self.my_tasks.append(new_task)

        self.send_message(f"\nNew task by {self.port}")
        self.send_message(f"\nTask{new_task.id}: {new_task.description}")
        for peer in self.peers:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', peer))
                task_str = f"{new_task.id}:{new_task.description}:{new_task.author}:{','.join(str(node) for node in new_task.accepted_nodes)}:{new_task.complete}"
                s.send(f'T:{task_str}'.encode('utf-8'))
                s.send(f'i:{self.global_task_id}'.encode('utf-8'))
                s.close()
            except Exception as e:
                pass
        print(self.available_tasks)
        return None

    def accept_task(self, task_id):
        import pdb
        pdb.set_trace()
        if self.history_tasks[int(task_id)].accepted_nodes[0] == self.port:
            pass

        if self.history_tasks[int(task_id)].accepted_nodes[1] != None:
            print("Task full")
            return


        else:
            if not self.task_exists(task_id):
                print("Task not found")
                return

            for peer in self.peers:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(('127.0.0.1', peer))
                    # self.available_tasks[int(task_id)]
                    s.send(f'S:{self.port}:{task_id}'.encode('utf-8')) # send syncronize_tasks
                    self.send_message(f'{self.port} has accepted task {task_id}')
                except Exception as e:
                    pass

            if self.history_tasks[int(task_id)].accepted_nodes[0] == None:
                self.available_tasks[int(task_id)].accepted_nodes[0] = self.port
                self.history_tasks[int(task_id)].accepted_nodes[0] = self.port

            # elif self.available_tasks[int(task_id)].accepted_nodes[0] == self.port:

            else:
                self.history_tasks[int(task_id)].accepted_nodes[1] = self.port = self.port
                self.available_tasks[int(task_id)].accepted_nodes[1] = self.port

            self.accepted_tasks.append(self.available_tasks[int(task_id)])
            self.available_tasks.pop(int(task_id))

    def syncronize_tasks(self, data):
        print("\nSyncronizing...")
        data = data.split(":")
        port = data[0]
        task_id = int(data[1])

        for task in self.available_tasks:
            if task.id == int(task_id):
                print("aN0 ", task.accepted_nodes[0])
                if task.accepted_nodes[0] == None:
                    task.accepted_nodes[0] = int(port)
                else:
                    task.accepted_nodes[1] = int(port)

        for task in self.accepted_tasks:
            if task.id == int(task_id):
                if task.accepted_nodes[0] == None:
                    task.accepted_nodes[0] = int(port)
                else:
                    task.accepted_nodes[1] = int(port)

        for task in self.history_tasks:
            if task.id == int(task_id):
                print("aN0 ", task.accepted_nodes[0])
                if task.accepted_nodes[0] == None:
                    task.accepted_nodes[0] = int(port)
                else:
                    task.accepted_nodes[1] = int(port)

        for task in self.history_tasks:
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

    def list_my_tasks(self):
        for task in self.my_tasks:
            print(str(task))



import os
import time
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
        self.given_tasks = []
        self.my_tasks = []
        self.global_task_id = 0
        self.balance = 10
        self.stake = 0
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', self.port))


    # COMPONENTE DA REDE P2P


    def handle_peer(self, client_socket):
        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                else:
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

    def send_to_peer(self, msg, peer):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', int(peer)))
        s.send(f'r:{msg}'.encode('utf-8'))
        s.close()

    def listen(self):
        self.server_socket.listen()
        self.server_socket.settimeout(1)  # Set a timeout of 1 second
        while not self.closed:
            try:
                client_socket, addr = self.server_socket.accept()
                header = client_socket.recv(2).decode('utf-8')
                data = client_socket.recv(1024).decode('utf-8')
                if header == 'P:': # connect to peer
                    self.peers.append(int(data))
                    threading.Thread(target=self.handle_peer, args=(client_socket,)).start()
                elif header == 'M:': # send message
                    print(f'\n{data}')

                elif header == 'i:':
                    self.global_task_id = int(data)

                elif header == 'T:': # new task
                    task_obj = Task.from_string(data)
                    self.given_tasks.append(task_obj)

                elif header == 'v:': # validator
                    self.send_to_peer(self.stake, data)

                elif header == 'w:': # work on task
                    print("got header w")
                    self.working_on_task()

                elif header == 'R:': # reward
                    self.balance = self.balance + int(data)
                    print("got reward")




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
            except Exception as e:
                pass


    #COMPONENTE DAS TASKS

    def make_task(self, description):
        menu = {
            "1": {"difficulty": "Tier A", "price": 5},
            "2": {"difficulty": "Tier B", "price": 10},
            "3": {"difficulty": "Tier C", "price": 15}
        }
        tier = input("""
        Welcome to the Menu:
        Please select an option:
        1. Tier A - $5
        2. Tier B - $10
        3. Tier C - $15
        """)
        selected_option = input("Option: ")
        if selected_option in menu:
            tier = menu[selected_option]
            if self.balance >= tier["price"]:
                self.balance -= tier["price"]
                print(f"{tier['difficulty']} purchased successfully!")
                print("Defining validator")
                assigned_n = random.sample([peer for peer in self.peers if peer != self.port], k=4)

                # assigns the validator based on who has the most staked coin from assigned_n

                validator_peer = None
                max_stake = float('-inf')


                for peer in assigned_n:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect(('127.0.0.1', peer))
                        s.send(f'v:{self.port}'.encode('utf-8'))
                        self.server_socket.listen()
                        while not self.closed:
                            client_socket, addr = self.server_socket.accept()
                            header = client_socket.recv(2).decode('utf-8')
                            data = client_socket.recv(1024).decode('utf-8')
                            if header == 'r:':
                                stake = int(data)
                                if stake > max_stake:
                                    max_stake = stake
                                    validator_peer = peer
                        # self.server_socket.close()

                    except:
                        pass

                print("validator set")
                new_task = Task(self.global_task_id,description, self.port, assigned_n, validator_peer, tier )
                self.global_task_id += 1
                new_task.assigned_nodes = assigned_n
                # Send the task information to the assigned nodes
                for peer in assigned_n:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect(('127.0.0.1', peer))
                        task_str = f"{new_task.id}:{new_task.description}:{new_task.author}:{','.join(str(node) for node in new_task.assigned_nodes)}:{new_task.complete}:{new_task.validator}:{new_task.difficulty}"
                        s.send(f'T:{task_str}'.encode('utf-8'))
                        s.send(f'i:{self.global_task_id}'.encode('utf-8'))
                        # s.close()
                    except Exception as e:
                        pass
                self.notify_assigned_nodes(assigned_n)
                self.my_tasks.append(new_task)

                self.clear_screen()
                print("Waiting for workers..", end='', flush=True)

                workers_complete = 0
                # for peer in assigned_n:
                try:
                    # s.send(f'c:{self.port}'.encode('utf-8'))
                    while workers_complete != 4:
                        self.server_socket.listen()
                        client_socket, addr = self.server_socket.accept()
                        header = client_socket.recv(2).decode('utf-8')
                        if header == 'c:':
                            print("got worker ping")
                            workers_complete += 1
                            print(workers_complete)

                except Exception as e:
                    print("something happened getting worker complete packets\n", e)

                for peer in assigned_n:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect(('127.0.0.1', peer))

                        if tier["difficulty"] == "Tier A":
                            print("sending")
                            s.send(f'R:{1}'.encode('utf-8'))
                            print("giving reward")
                            # s.close()

                        if tier["difficulty"] == "Tier B":
                            s.send(f'R:{2}'.encode('utf-8'))
                            print("giving reward")
                            # s.close()

                        if tier["difficulty"] == "Tier C":
                            s.send(f'R:{3}'.encode('utf-8'))
                            print("giving reward")
                            # s.close()

                        # self.server_socket.close()

                    except Exception as e:
                        print("something went wrong with rewards\n", e)

                try:
                    print("validator ", validator_peer)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(('127.0.0.1', validator_peer))
                    if tier["difficulty"] == "Tier A":
                        print("giving reward")
                        s.send(f'R:{1}'.encode('utf-8'))
                        # s.close()

                    if tier["difficulty"] == "Tier B":
                        s.connect(('127.0.0.1', validator_peer))
                        s.send(f'R:{2}'.encode('utf-8'))
                        print("giving reward")
                        # s.close()

                    if tier["difficulty"] == "Tier C":
                        s.connect(('127.0.0.1', validator_peer))
                        s.send(f'R:{3}'.encode('utf-8'))
                        print("giving reward")
                        # s.close()

                        # self.server_socket.close()
                except Exception as e:
                    print(e)

                # Number of seconds for the timer

                print("\nTask completed!")



            else:
                print(f"Insufficient balance to purchase {tier['difficulty']}.")
                return
        else:
            print("Invalid option selected.")



    def notify_assigned_nodes(self, assigned_n):
        message = "You have been assigned task.\n Starting work shortly."
        for peer in assigned_n:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', peer))
                s.send(f'w:{""}'.encode('utf-8'))
                s.send(f'M:{message}'.encode('utf-8'))
                s.close()
            except Exception as e:
                pass


    def clear_screen(self):
        # Clear command for Windows
        if os.name == 'nt':
            _ = os.system('cls')
        # Clear command for Unix/Linux/MacOS
        else:
            _ = os.system('clear')

    def working_on_task(self):
        self.clear_screen()
        print("Working on task...", end='', flush=True)

        # Number of seconds for the timer
        timer_duration = random.randint(1, 10)
        for _ in range(timer_duration):
            time.sleep(1)
            print(".", end='', flush=True)
        # self.clear_screen()

        author = self.given_tasks[0].get_author()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', int(author)))
        print("connected to author")
        s.send(f'c:{""}'.encode('utf-8'))
        print("sendind c:")
        print("\nTask completed!")
        self.balance = self.balance + self.stake
        self.stake = 0
        print("stake ", self.stake)

    def list_given_tasks(self):
        for task in self.given_tasks:
            print(task)
            # print(str(task))

    def list_my_tasks(self):
        for task in self.my_tasks:
            print(str(task))

    def get_balance(self):
        print(f"\nYour balance is - {self.balance}")

    def print_stake(self):
        print(f"\nYour stake is - {self.stake}")

    def get_stake(self):
        return self.stake

    def add_balance(self, amount):
        self.balance += amount
        print(f"\nBalance of {self.port} updated to {self.balance}")

    def add_stake(self):

        amount = int(input("How many tokens: "))
        self.stake += amount
        self.balance = self.balance - self.stake

    def exit(self):
        print(f"\nNode {self.port} exited")
        self.closed = True
        self.server_socket.close()
        sys.exit()

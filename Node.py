import os
import time
import socket
import threading
import sys
from Task import Task
from Block import *
from Blockchain import *
import hashlib
import random
import pickle
# from flask import Flask, render_template




class Node():
    def __init__(self, port):
        self.port = port
        self.peers = []
        self.closed = False
        self.given_tasks = []
        self.my_tasks = []
        self.global_task_id = 0
        self.balance = 100
        self.stake = 0
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', self.port))
        self.blockchain = Blockchain()
        self.wallet = hashlib.sha256(str(self.port).encode()).hexdigest()


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
        node_who_completed_task = 0
        nodes_rewarded = 0
        successful_validations = 0
        self.server_socket.listen()
        self.server_socket.settimeout(1)  # Set a timeout of 1 second
        while not self.closed:
            try:
                client_socket, addr = self.server_socket.accept()
                header = client_socket.recv(2).decode('utf-8')
                data = client_socket.recv(10000).decode('utf-8')
                if header == 'P:': # connect to peer
                    self.peers.append(int(data))
                    threading.Thread(target=self.handle_peer, args=(client_socket,)).start()
                elif header == 'M:': # send message
                    print(f'\n{data}')

                elif header == 'i:':  # idk what this is
                    self.global_task_id = int(data)

                elif header == 'T:': # new task
                    task_obj = Task.from_string(data)
                    self.given_tasks.append(task_obj)

                elif header == 'v:': # give me your stake values so i can decide who's the validator
                    self.send_to_peer(self.stake, data)

                elif header == 'w:': # work on task
                    print("got header w")
                    self.working_on_task()

                elif header == 'R:': # if you get this you can be rewared
                    self.balance = self.balance + int(data)
                    self.got_reward()

                elif header == 'c:':  #  this is what nodes send when they finish working on a task
                    node_who_completed_task += 1
                    print("[Node: ",node_who_completed_task,", status complete]")
                    if node_who_completed_task == 4:
                        node_who_completed_task = 0
                        self.reward()

                elif header == 'p:': # this is sent from workers to validators to inform they have been payed
                    print("got p:")
                    print(nodes_rewarded)
                    nodes_rewarded += 1
                    if nodes_rewarded == 3:
                        nodes_rewarded = 0
                        self.create_block()

                elif header == 'x:':
                    data = Block.from_string(data)
                    print(data)
                    self.validate(data)

                elif header == 'o:':
                    successful_validations +=1
                    if successful_validations == len(self.peers)-1:
                        successful_validations = 0
                        self.blockchain.add_block(data)


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

        print("""
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
                assigned_n = random.sample([peer for peer in self.peers if peer != self.port], k=4)

                # assigns the validator based on who has the most staked coin from assigned_n

                print("[Setting validator]")
                validator_peer = self.get_validator_peer(assigned_n)
                print("[Validator set]")
                time.sleep(1)
                new_task = Task(self.global_task_id, description, self.port, assigned_n, validator_peer, tier)
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
                        s.close()
                    except Exception as e:
                        pass
                self.notify_assigned_nodes(assigned_n)
                self.my_tasks.append(new_task)
                self.clear_screen()
                time.sleep(11)
                self.list_my_tasks()
            else:
                print(f"Insufficient balance to purchase {tier['difficulty']}.")
                return
        else:
            print("Invalid option selected.")
            return None



    def get_validator_peer(self, assigned_n):

        validator_peer = None
        max_stake = 0

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
            except:
                pass
        print("validator in decision ", validator_peer)
        return validator_peer

    def reward(self):
        task = self.my_tasks[-1]
        assigned_n = task.assigned_nodes
        tier = task.difficulty
        validator_peer = task.validator
        for peer in assigned_n:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', peer))

                if tier["difficulty"] == "Tier A":
                    s.send(f'R:{1}'.encode('utf-8'))
                    print("giving reward")

                if tier["difficulty"] == "Tier B":
                    s.send(f'R:{2}'.encode('utf-8'))
                    print("giving reward")

                if tier["difficulty"] == "Tier C":
                    s.send(f'R:{3}'.encode('utf-8'))
                    print("giving reward")

                s.close()
            except Exception as e:
                print("something went wrong with rewards\n", e)

        try:
            print("validator ", validator_peer)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', validator_peer))
            if tier["difficulty"] == "Tier A":
                print("giving reward")
                s.send(f'R:{1}'.encode('utf-8'))

            if tier["difficulty"] == "Tier B":
                s.send(f'R:{2}'.encode('utf-8'))
                print("giving reward")

            if tier["difficulty"] == "Tier C":
                s.send(f'R:{3}'.encode('utf-8'))
                print("giving reward")

            s.close()
        except Exception as e:
            print(e)

        print("\nTask completed!")

    def notify_assigned_nodes(self, assigned_n):
        message = "-- You have been assigned task.]\n -- Starting work shortly."
        time.sleep(1)
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
        self.list_given_tasks()
        # self.clear_screen()
        print("Working on task...", end='', flush=True)

        # Number of seconds for the timer
        timer_duration = random.randint(1, 10)
        for _ in range(timer_duration):
            time.sleep(1)
            print(".", end='', flush=True)
        # self.clear_screen()

        author = self.given_tasks[-1].get_author()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', int(author)))
        s.send(f'c:{""}'.encode('utf-8'))
        print("\n-- Task completed!")
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
        print(f"Wallet [{self.wallet}]\nBalance: {self.balance}")

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



    def create_block(self):
        author = self.given_tasks[-1].author
        validator = self.given_tasks[-1].validator
        task = self.given_tasks[-1]
        peers = self.given_tasks[-1].assigned_nodes
        tier = task.difficulty
        print("tier: ", tier)
        transactions = []
        previous_hash = self.blockchain.get_latest_block().hash
        if tier[0] == "Tier A":
            transactions.append(f"1 token from {author} to {validator}")
            for peer in peers:
                transactions.append(f"1 token from {author} to {peer}")

        if tier[0] == "Tier B":
            transactions.append(f"2 token from {author} to {validator}")
            for peer in peers:
                transactions.append(f"2 token from {author} to {peer}")

        if tier[0] == "Tier C":
            transactions.append(f"3 token from {author} to {validator}")
            for peer in peers:
                transactions.append(f"3 token from {author} to {peer}")

        data = [author, validator, task, peers, transactions, previous_hash]
        print("this is data:\n\n\n")
        print(data)
        block = self.blockchain.generate_new_block(data)
        # print(self.blockchain.get_blockchain())
        # dump = pickle.dumps(block)

        for peer in self.peers:
            if peer != self.port:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', peer))
                s.send(f'x:{block}'.encode('utf-8'))

    def got_reward(self):
        task = self.given_tasks[-1]
        validator_peer = task.validator
        if self.port != validator_peer:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', int(validator_peer)))
            s.send(f'p:{""}'.encode('utf-8'))
            print("got reward")
            s.close()
        else:
            pass

    def validate(self, block):
        # print(block.content)
        print(type(block.content))
        print("this is hash of 1 ", self.blockchain.get_latest_block().hash, type(self.blockchain.get_latest_block().hash))
        print("this is hash of 2", block.previous_hash, type(block.previous_hash))
        if str(self.blockchain.get_latest_block().hash) != str(block.previous_hash):
            print("Validation failed")
        else:
            for peer in self.peers:
                if peer != self.port:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(('127.0.0.1', peer))
                    s.send(f'o:{block}'.encode('utf-8'))
            self.blockchain.validate_blockchain()
            self.blockchain.add_block(block)
            print("Validated successfully")





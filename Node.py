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
import datetime


class Node():
    def __init__(self, port, gui=None):
        self.gui = gui
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
        # print(self.server_socket)
        self.blockchain = Blockchain()
        self.wallet = hashlib.sha256(str(self.port).encode()).hexdigest()
        self.globa_validator = 0
        threading.Thread(target=self.listen).start()


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
        print(self.peers)
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
        msg = str(msg) +":"+ str(self.port)
        s.send(f'r:{msg}'.encode('utf-8'))
        s.close()

    def show_peers(self):
        peers = []
        for _ in self.peers:
            peers.append(_)
        return peers


    def listen(self):
        node_who_completed_task = 0
        nodes_rewarded = 0
        stakes = []
        successful_validations = 0
        self.server_socket.listen()
        self.server_socket.settimeout(1)  # Set a timeout of 1 second
        while not self.closed:
            try:
                client_socket, addr = self.server_socket.accept()
                # print(self.server_socket)
                # print("client_socket: ", client_socket)
                # print("myaddr: ", addr)
                header = client_socket.recv(2).decode('utf-8')
                data = client_socket.recv(10000).decode('utf-8')
                if header == 'P:': # connect to peer
                    self.peers.append(int(data))
                    threading.Thread(target=self.handle_peer, args=(client_socket,)).start()
                elif header == 'M:': # send message
                    if self.gui:
                        self.gui.add_message(data)
                    else:
                        print(f'\n{data}')

                elif header == 'i:':  # idk what this is
                    self.global_task_id = int(data)

                elif header == 'T:': # new task
                    task_obj = Task.from_string(data)
                    self.given_tasks.append(task_obj)

                elif header == 'v:': # give me your stake values so i can decide who's the validator
                    print("i got header v")
                    # print("data is ", data, type(data))
                    self.send_to_peer(self.stake, data)

                elif header == 'w:': # work on task
                    # print("got header w")
                    if self.gui:
                        self.gui.working_on_task()
                    else:
                        self.working_on_task()

                elif header == 'R:': # if you get this you can be rewared
                    self.balance = self.balance + int(data)
                    self.got_reward()

                elif header == 'c:':  #  this is what nodes send when they finish working on a task
                    if self.gui:
                        self.gui.add_message(data)
                        node_who_completed_task += 1
                        print("[Node: ",node_who_completed_task,", status complete]")
                        if node_who_completed_task == 4:
                            node_who_completed_task = 0
                            self.reward()
                    else:
                        node_who_completed_task += 1
                        print("[Node: ",node_who_completed_task,", status complete]")
                        if node_who_completed_task == 4:
                            node_who_completed_task = 0
                            self.reward()

                elif header == 'p:': # this is sent from workers to validators to inform they have been payed
                    # print("got p:")
                    # print(nodes_rewarded)
                    nodes_rewarded += 1
                    if nodes_rewarded == 3:
                        nodes_rewarded = 0
                        self.create_block()
                        # break

                elif header == 'b:': # gets block string
                    data = Block.from_string(data)
                    print(data)
                    self.validate(data)

                elif header == 'o:':  # sent from all peers to the validator informing they agree on validity
                    successful_validations +=1
                    if successful_validations == len(self.peers)-1:
                        successful_validations = 0
                        self.blockchain.add_block(Block.from_string(data))
                        self.clear_screen()
                        print("Block successfully added to the Blockchain")

                elif header == 'r:':  # asserts validator
                    print("got r")
                    data = data.split(":")
                    stakes.append(data)
                    print(stakes)
                    current_peer = 0
                    for peer in stakes:
                        # print(peer[0])
                        # print(peer[1])
                        # print(type(int(peer[0])))8.1.65:3533
                        if int(peer[0]) > int(current_peer):
                            current_peer = peer[1]
                            print(current_peer)
                            # current_stake = peer[0]
                            # print("current peer: ",current_peer)
                    self.globa_validator = int(current_peer)
                    self.send_new_validator(self.globa_validator)
                    print("task validator: ", self.globa_validator)

                elif header == "n:":
                    print("got n")
                    self.globa_validator = int(data)
                    print("new validator: ", self.globa_validator)


            except socket.timeout:
                continue
            except OSError as e:
                break  # If the server socket is closed, break the loop


    def send_new_validator(self, validator):
        for i in self.peers:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', i))
            s.send(f'n:{validator}'.encode('utf-8'))
            s.close()

    def connect_to_peers(self, local = True):
        if local:
            print("local")
            for i in range(8000, self.port):
                print(i)
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1/2)  # Add a timeout to the socket
                    s.connect(('127.0.0.1', i))
                    s.send(f'P:{self.port}'.encode('utf-8'))
                    self.peers.append(i)
                    threading.Thread(target=self.handle_peer, args=(s,)).start()
                except Exception as e:
                    pass
        else:
            print("unlocal")
            for i in range(8000, self.port):
                print(i)
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

    def make_task(self, description, selection):
        if self.gui:
            self.continue_gui_task(description, selection)

        else:
            self.continue_cli_task(description, selection)

    def continue_gui_task(self, description, selection):
        tier = selection
        if self.balance >= selection:
            self.balance -= selection
            # print(f"{tier['difficulty']} purchased successfully!")
            self.gui.add_message("purchased successfully!")

            assigned_n = random.sample([peer for peer in self.peers if peer != self.port], k=4)

            # assigns the validator based on who has the most staked coin from assigned_n

            print("[Setting validator]")
            self.send_validator_header(assigned_n)
            time.sleep(1)
            validator_peer = self.globa_validator
            # print("validator peer after global ", validator_peer)
            print(validator_peer)
            if validator_peer != 0:
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
            else:
                print("Failed getting validator... try again.")
        else:
            print(f"Insufficient balance to purchase {tier['difficulty']}.")
            return

    def send_task_done_from_gui(self):
        author = self.given_tasks[-1].get_author()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', int(author)))
        s.send(f'c:{""}'.encode('utf-8'))
        s.close()
        print("\n-- Task completed!")
        self.balance = self.balance + self.stake
        self.stake = 0

    def continue_cli_task(self, description, tier):
        if self.balance >= int(tier):
            self.balance -= int(tier)
            print("purchased successfully!")
            assigned_n = random.sample([peer for peer in self.peers if peer != self.port], k=4)

            # assigns the validator based on who has the most staked coin from assigned_n

            print("[Setting validator]")
            self.send_validator_header(assigned_n)
            time.sleep(1)
            validator_peer = self.globa_validator
            # print("validator peer after global ", validator_peer)
            print(validator_peer)
            if validator_peer != 0:
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
            else:
                print("Failed getting validator... try again.")
        else:
            print(f"Insufficient balance to purchase {tier['difficulty']}.")
            return

    # def get_validator_peer(self, validator):
    #     return int(validator)

    def send_validator_header(self, assigned_n):

        print("assigned nodes: ", assigned_n)
        for current_peer in assigned_n:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer = current_peer
            s.connect(('127.0.0.1', peer))
            s.send(f'v:{self.port}'.encode('utf-8'))
            s.close()
        # print("validator in decision ", self.globa_validator)


    def reward(self):
        task = self.my_tasks[-1]
        assigned_n = task.assigned_nodes
        tier = task.difficulty
        print(tier)
        print(type(tier))
        # validator_peer = task.validator
        for peer in assigned_n:
            if peer != task.author:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(('127.0.0.1', peer))

                    # if tier["difficulty"] == "Tier A":
                    if tier == 5:
                        s.send(f'R:{1}'.encode('utf-8'))
                        print("giving reward")
                        s.close()

                    if tier == 10:
                        s.send(f'R:{2}'.encode('utf-8'))
                        print("giving reward")
                        s.close()

                    if tier == 15:
                        s.send(f'R:{3}'.encode('utf-8'))
                        print("giving reward")
                        s.close()

                except Exception as e:
                    print("something went wrong with rewards\n", e)

        try:
            print("validator in reward ", self.globa_validator)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', self.globa_validator))
            if tier == 5:
                print("giving reward")
                s.send(f'R:{1}'.encode('utf-8'))
                s.close()

            if tier == 10:
                s.send(f'R:{2}'.encode('utf-8'))
                print("giving reward")
                s.close()

            if tier == 15:
                s.send(f'R:{3}'.encode('utf-8'))
                print("giving reward")
                s.close()

        except Exception as e:
            print(e)

        print("\nTask completed!")

    def notify_assigned_nodes(self, assigned_n):
        time.sleep(1)
        for peer in assigned_n:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', peer))
                s.send(f'w:{""}'.encode('utf-8'))
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
        # self.list_given_tasks()
        self.clear_screen()
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
        s.close()
        print("\n-- Task completed!")
        self.balance = self.balance + self.stake
        self.stake = 0
        print("stake ", self.stake)
        return None

    def list_given_tasks(self):
        tasks = []
        for task in self.given_tasks:
            print(task)
            tasks.append(task)
        return tasks

    def list_my_tasks(self):
        tasks = []
        for task in self.my_tasks:
            print(str(task))
            tasks.append(task)
        return tasks

    def get_balance(self):
        print(f"Wallet [{self.wallet}]\nBalance: {self.balance}")
        return self.balance

    def print_stake(self):
        print(f"\nYour stake is - {self.stake}")

    def get_stake(self):
        return self.stake

    def add_balance(self, amount):
        self.balance += amount
        print(f"\nBalance of {self.port} updated to {self.balance}")

    def add_stake(self, amount):
        self.stake += int(amount)
        self.balance = self.balance - self.stake

    def exit(self):
        print(f"\nNode {self.port} exited")
        self.closed = True
        self.server_socket.close()
        sys.exit()



    def create_block(self):
        timestamp = datetime.datetime.now()
        author = self.given_tasks[-1].author
        validator = self.globa_validator
        task = self.given_tasks[-1]
        peers = self.given_tasks[-1].assigned_nodes
        tier = int(task.difficulty)
        transactions = []
        previous_hash = self.blockchain.get_latest_block().hash
        if tier == 1:
            transactions.append(f"1 token from {author} to {validator}")
            for peer in peers:
                transactions.append(f"1 token from {author} to {peer}")

        if tier == 2:
            transactions.append(f"2 token from {author} to {validator}")
            for peer in peers:
                transactions.append(f"2 token from {author} to {peer}")

        if tier == 3:
            transactions.append(f"3 token from {author} to {validator}")
            for peer in peers:
                transactions.append(f"3 token from {author} to {peer}")


        def calculate_hash(transactions):
            # Convert each transaction to a string and calculate the hash of the concatenated transactions
            concatenated = ''.join(str(t) for t in transactions).encode()
            return hashlib.sha256(concatenated).hexdigest()

        transaction_hashes = []
        print(transactions)
        for transaction in transactions:
            transaction_hashes.append(calculate_hash([transaction]))

        while len(transaction_hashes) > 1:
            new_hashes = []
            for i in range(0, len(transaction_hashes), 2):
                pair = transaction_hashes[i:i+2]
                concatenated = ''.join(pair).encode()
                new_hash = calculate_hash(concatenated)
                new_hashes.append(new_hash)
            transaction_hashes = new_hashes

        merkle_root = transaction_hashes[0]



        data = [author, validator, task, peers, transactions, timestamp, previous_hash, merkle_root]
        block = self.blockchain.generate_new_block(data)
        self.clear_screen()

        for peer in self.peers:
            if peer != self.port:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', peer))
                s.send(f'b:{block}'.encode('utf-8'))
                s.close()

    def got_reward(self):
        # task = self.given_tasks[-1]
        validator_peer = self.globa_validator
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
        if str(self.blockchain.get_latest_block().hash) != str(block.previous_hash):
            print("Validation failed")
        else:
            try:
                task = self.given_tasks[-1]
                # validator_peer = task.validator
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', int(self.globa_validator)))
                s.send(f'o:{block}'.encode('utf-8'))
                s.close()
                self.blockchain.validate_blockchain()
                self.blockchain.add_block(block)
                self.clear_screen()
                print("Validated successfully")
                # return None
            except:
                task = self.my_tasks[-1]
                # validator_peer = task.validator
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', int(self.globa_validator)))
                s.send(f'o:{block}'.encode('utf-8'))
                s.close()
                self.blockchain.validate_blockchain()
                self.blockchain.add_block(block)
                self.clear_screen()
                print("Validated successfully")
                # return None


    def view_blockchain(self):
        # print(self.blockchain.get_latest_block())
        blocks = []
        for block in range(self.blockchain.get_blockchain_height()):
            print(self.blockchain.get_block(block))
            blocks.append(self.blockchain.get_block_string(block))
        return blocks




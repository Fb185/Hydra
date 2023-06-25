import datetime as date
from Block import Block
import random
from ledger import Ledger

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        # self.stakeholders = {}  # Dictionary to store stakeholders and their stakes
        # self.ledger = Ledger()

    def create_genesis_block(self):
        return Block(0,"0", "0", "Genesis Block")

    def get_blockchain_height(self):
        return len(self.chain)

    def get_latest_block(self):
        return self.chain[-1]

    def get_blockchain(self):
        return self.chain

    def get_block_string(self, block):
        block =  self.chain[block]
        block_string = (f"previous hash: {block.previous_hash}\nhash: {block.hash}\nindex: {block.index}\ncontent: {block.content}")
        return block_string

    def get_block(self, block):
        block =  self.chain[block]
        print(f"previous hash: {block.previous_hash}\nhash: {block.hash}\nindex: {block.index}\ncontent: {block.content}\n\n")
        return block



    def add_block(self, new_block):
        self.chain.append(new_block)

    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.previous_hash != previous_block.hash:
                return False
        return True




    def generate_new_block(self, content):
        # timestamp = date.datetime.now()
        previous_hash = self.get_latest_block().hash
        index =  int(self.get_latest_block().index) +1
        new_block = Block(previous_hash, 0, index, content)
        new_block.calculate_hash()
        print("New block created:\n" + str(new_block))
        return new_block




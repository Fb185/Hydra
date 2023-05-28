from hashlib import *
import datetime as date
#from p2p.Node import *
from Block import Block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.nodes = []  # Store the nodes in a list
        self.stake = {}  # Store the stake of each node

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        self.chain.append(new_block)
        
    def elected(self):
        return max(self.stake, key=self.stake.get)

    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    
    def generate_new_block(self, data):
        index = len(self.chain)
        timestamp = date.datetime.now()
        previous_hash = self.get_latest_block().hash if len(self.chain) > 0 else "0"
        new_block = Block(index, timestamp, data, previous_hash)
        node_id = self.elected()
        if node_id in self.nodes:
            self.add_block(new_block)
            print("New block created:\n" + str(new_block))
            return True
        else:
            return False



if __name__ == "__main__":
        
    blockchain = Blockchain()


# Testing
if __name__ == "__main__":
    # Create a blockchain instance
    blockchain = Blockchain()

    # Set node ID and stake
    node_id = "Node1"
    stake = 100

    # Add node to the blockchain
    blockchain.nodes.append(node_id)
    blockchain.stake[node_id] = stake

    # Generate a new block
    data = "Block data"
    blockchain.generate_new_block(data) 
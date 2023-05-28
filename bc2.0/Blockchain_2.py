from hashlib import *
import datetime as date
from p2p.Node import *
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














"""

if __name__ == "__main__":
        
    blockchain = Blockchain()

    # Sample stake values and node IDs
    stake_values = {
        "node1": 100,
        "node2": 150,
        "node3": 200,
        "node4": 125
    }

    # Add nodes and their corresponding stake values to the blockchain
    for node_id, stake in stake_values.items():
        blockchain.nodes.append(node_id)
        blockchain.stake[node_id] = stake

    # generate new block with data
    blockchain.generate_new_block("Block 1 data")

    # validate blockchain
    print("Is blockchain valid? " + str(blockchain.validate_blockchain()))
    
    # Print the __str__ representation of the Block
    new_block = Block(1, date.datetime.now(), "Block 1 data", blockchain.get_latest_block().hash)
    print(str(new_block))
    """
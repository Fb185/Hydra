import datetime as date
from Block import Block
import random


class Blockchain:
    def __init__(self):
        self.chain = []

    def create_genesis_block(self):
        return Block(None, date.datetime.now(), "0", "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        self.chain.append(new_block)

    def validate_blockchain(self, data):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Validate block hash
            merkle_tree = Block(None, None, None, data)
            if current_block.hash != merkle_tree.build_merkle_tree(data):
                return False
            # Validate previous hash
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    
    def generate_new_block(self, data):
        index = len(self.chain)
        timestamp = date.datetime.now()
        if len(self.chain) == 0:
            previous_hash = 0
            self.create_genesis_block()
        else:
            previous_hash = self.get_latest_block().hash 
        new_block = Block(previous_hash, timestamp, index, data)
        self.add_block(new_block)
        print("New block created:\n" + str(new_block))
    


"""
# Testing
if __name__ == "__main__":
    blockchain = Blockchain()

    # Generate five blocks
    num_blocks = 5
    for i in range(num_blocks):
        data = ["Transactvxczvxion 1", "Tranasdasdsaction 2", "Transaeqweqwection 3", "Transactwqeqweion 2", "Transacqweqwtion 3", "Transaasdasdction 2", "Transaction 3"]
        random.shuffle(data)
        new_block = blockchain.generate_new_block(data)
        print("New block created:\n" + str(new_block))
    
    # Validate the blockchain
    is_valid = blockchain.validate_blockchain(data)
    print("Blockchain is valid:", is_valid)

""" 
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




# Testing
if __name__ == "__main__":
    blockchain = Blockchain()
    # print("blockchain: ", blockchain.get_latest_block())

    # Generate five blocks
    num_blocks = 5
    for i in range(num_blocks):
        # import pdb
        # pdb.set_trace()
        data = ["Transaction 1", "Transaction 2", "Transaction 3", "Transaction 4", "Transaction 5", "Transaction 6", "Transaction 7"]
        random.shuffle(data)
        new_block = blockchain.generate_new_block(data)
        blockchain.add_block(new_block)
        # merkle_tree = new_block.view_merkle_tree()
        # print("Merkle Tree:", merkle_tree)        # time.sleep(2)

    # Validate the blockchain
    is_valid = blockchain.validate_blockchain()
    print("Blockchain is valid:", is_valid)

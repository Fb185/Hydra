import datetime as date
from Block import Block
import random
import time
from ledger import Ledger

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.stakeholders = {}  # Dictionary to store stakeholders and their stakes
        self.ledger = Ledger()

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        self.chain.append(new_block)

    def validate_blockchain(self, content):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            # Validate block hash
            merkle_tree = Block(None, None, None, content)
            # if current_block.hash != merkle_tree.build_merkle_tree(data):
            if current_block.hash != merkle_tree.build_merkle_tree(current_block.content)[0]:
                return False
            # Validate previous hash
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def create_genesis_block(self):
        return Block(None, date.datetime.now(), "0", "Genesis Block")


    def generate_new_block(self, content):
        timestamp = date.datetime.now()
        previous_hash = self.get_latest_block().hash

        # Select a block creator based on stake
        # creator = self.select_block_creator()
        new_block = Block(previous_hash, timestamp, int(self.get_latest_block().index) + 1, content)
        self.add_block(new_block)
        self.ledger.add_block(new_block)
        print("New block created:\n" + str(new_block))

    def select_block_creator(self):
        total_stake = sum(self.stakeholders.values())
        random_number = random.randint(1, total_stake)
        stake_accumulator = 0

        for stakeholder, stake in self.stakeholders.items():
            stake_accumulator += stake
            if stake_accumulator >= random_number:
                return stakeholder

    def get_stakeholder(self, creator):
        if creator not in self.stakeholders:
            self.stakeholders[creator] = random.randint(1, 100)
        return self.stakeholders[creator]

# Testing
if __name__ == "__main__":
    blockchain = Blockchain()
    print("blockchain: ", blockchain.get_latest_block())

    # Generate five blocks
    num_blocks = 5
    for i in range(num_blocks):
        data = ["Transactvxczvxion 1", "Tranasdasdsction 2", "Transaeqweqwction 3", "Transactwqeqweion 2", "Transacqweqwtion 3", "Tranaasdasdction 2", "Transactio 3"]
        random.shuffle(data)
        new_block = blockchain.generate_new_block(data)
        time.sleep(2)

    # Validate the blockchain
    is_valid = blockchain.validate_blockchain(data)
    print("Blockchain is valid:", is_valid)


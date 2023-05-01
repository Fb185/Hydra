import hashlib
import datetime as date

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        hash_str = (str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode('utf-8')
        sha.update(hash_str)
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.delegates = ["Delegate1", "Delegate2", "Delegate3"]
        self.votes = {}

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def delegate_voting_power(self, delegate_name, voting_power):
        self.votes[delegate_name] = voting_power

    def get_delegate_with_most_votes(self):
        return max(self.votes, key=self.votes.get)

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
        previous_hash = self.get_latest_block().hash
        new_block = Block(index, timestamp, data, previous_hash)
        delegate_name = self.get_delegate_with_most_votes()
        if delegate_name in self.delegates:
            self.add_block(new_block)
            return True
        else:
            return False

blockchain = Blockchain()
blockchain.delegate_voting_power("Delegate1", 10)
blockchain.delegate_voting_power("Delegate2", 20)
blockchain.delegate_voting_power("Delegate3", 30)

# generate new block with data
blockchain.generate_new_block("Block 1 data")

# validate blockchain
print(blockchain.validate_blockchain())
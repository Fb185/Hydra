import hashlib
import datetime as date
from Node import Node
"""
merdas a lembrar

- o validador de cada bloco será um dos 3 workers que está a a realizar a task, 
que possuir o maior valor de stake

- esse vai ser o node responsavél por acionar a função add_block

- agora como é a validação do bloco é feita tem que se ver ainda

TODO - merkle tree ver como é que implementada, ficheiro a parte, dentro deste, etc ....

- os nodes vão ser identificados não por um id mas atarvés do port que lhes é atribuido
quando eles são inicializados

- pelo facto de numa merkle tree ter que obrigatoriamente haver um nomero par de leaf nodes eu 
sugiro que o numeor de pessoas que possam participar numa task sejam 4.
"""

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

    def __str__(self):
        return "Block Index: " + str(self.index) + "\nTimestamp: " + str(self.timestamp) + "\nData: " + str(self.data) + "\nHash: " + str(self.hash) + "\nPrevious Hash: " + str(self.previous_hash)

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.nodes = Node.ports
        self.stake = {}

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def validator(self, node_id, validator_prob):
        self.stake[node_id] = validator_prob

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
        previous_hash = self.get_latest_block().hash
        new_block = Block(index, timestamp, data, previous_hash)
        node_id = self.elected()
        if node_id in self.nodes:
            self.add_block(new_block)
            print("New block created:\n" + str(new_block))
            return True
        else:
            return False

blockchain = Blockchain()

# generate new block with data
blockchain.generate_new_block("Block 1 data")

# validate blockchain
print("Is blockchain valid? " + str(blockchain.validate_blockchain()))
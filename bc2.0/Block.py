from Merkletree import Merkletree
from Blockchain_2 import blockchain

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.index = index
        self.hash = Merkletree(None, None, data).build_merkle_tree(data)
        

    def __str__(self):
        return "Block Index: " + str(self.previous_hash) + "\nTimestamp: " + str(self.timestamp) + "\nData: " + str(self.index) + "\Hash: " + str(self.hash)

    # Test method to output the __str__ representation of a block
    def print_block_info(self):
        print(str(self))










# Parcela de teste para o Bloco
"""
if __name__ == "__main__":
    # Create a block
    block = Block(1, "2023-05-28 12:00:00", "Block data", "previous_hash")
    
    # Output the __str__ representation of the block
    block.print_block_info()
    """
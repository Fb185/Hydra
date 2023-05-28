from Merkletree import Merkletree

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.index = index
        self.hash = Merkletree(None, None, data).build_merkle_tree(data)
        

    def __str__(self):
        return "Block Index: " + str(self.previous_hash) + "\nTimestamp: " + str(self.timestamp) + "\nData: " + str(self.index) + "\nHash: " + str(self.hash)

    # Test method to output the __str__ representation of a block
    def print_block_info(self):
        print(str(self))


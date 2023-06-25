import hashlib

class Block:
    def __init__(self, previous_hash, hash, timestamp,  index, content):
        self.previous_hash = previous_hash
        self.index = index
        self.content = content
        self.hash = hash



    # @classmethod
    def from_string(block_string):
        print (block_string)
        previous_hash, hash, index, content = block_string.split(':')
        return Block(previous_hash, hash, int(index), content)


    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.previous_hash).encode('utf-8') +
                   str(self.index).encode('utf-8') +
                   str(self.content).encode('utf-8'))
        self.hash = sha.hexdigest()
        # return sha.hexdigest()



    def __str__(self):
        return f"{self.previous_hash}:{self.hash}:{self.index}:{self.content}"

import hashlib
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

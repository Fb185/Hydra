import hashlib

class Block:
    def __init__(self, previous_hash, timestamp, index, data):
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.index = index
        self.hash = self.build_merkle_tree(data)

    def calculate_hash(self, data):
        sha = hashlib.sha256()
        sha.update(data.encode('utf-8'))
        return sha.hexdigest()

    def build_merkle_tree(self, data):
        if len(data) == 1:
            return [self.calculate_hash(data[0])]

        # Recursive call to build left and right subtrees
        left_subtree = self.build_merkle_tree(data[:len(data)//2])
        right_subtree = self.build_merkle_tree(data[len(data)//2:])
        # Combine left and right subtrees hashes
        combined_hashes = left_subtree + right_subtree
        # Calculate parent hashes by hashing the concatenation of left and right hashes
        merkle_root = []
        for i in range(0, len(combined_hashes), 2):
            hash1 = combined_hashes[i]
            hash2 = combined_hashes[i+1] if i+1 < len(combined_hashes) else combined_hashes[i]
            parent_hash = self.calculate_hash(hash1 + hash2)
            merkle_root.append(parent_hash)

        return merkle_root
    
    def __str__(self):
        return "Previous Hash: " + str(self.previous_hash) + "\nTimestamp: " + str(self.timestamp) + "\Index: " + str(self.index) + "\nHash: " + str(self.hash)



import hashlib

class Block:
    def __init__(self, previous_hash, hash, timestamp, index, content):
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash(content)
        self.timestamp = timestamp
        self.index = index
        self.content = content


    @classmethod
    def from_string(cls, block_string):
        previous_hash, hash, timestamp, index, content = block_string.split(':')
        return cls(previous_hash, hash, timestamp, index, content )



    def calculate_hash(self, content):
        content_str = str(content)
        sha = hashlib.sha256()
        sha.update(content_str.encode('utf-8'))
        return sha.hexdigest()

    def build_merkle_tree(self, content):
        if len(content) == 1:
            return [self.calculate_hash(content[0])]

        # Recursive call to build left and right subtrees
        left_subtree = self.build_merkle_tree(content[:len(content)//2])
        right_subtree = self.build_merkle_tree(content[len(content)//2:])
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


    def view_merkle_tree(self):
        return self.build_merkle_tree(self.content)

    def __str__(self):
        return  str(self.previous_hash) + ":" + str(self.hash) + ":" + str(self.timestamp) + ":" + str(self.index) + ":" + str(self.content)



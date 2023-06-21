import hashlib

class Block:
    def __init__(self, previous_hash, timestamp, index, content):
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.index = index
        self.content = content
        self.hash = self.calculate_hash()




    @classmethod
    def from_string(cls, block_string):
        previous_hash, timestamp, index, content, hash = block_string.split(':')
        return cls(previous_hash, float(timestamp), int(index), content)


    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.previous_hash).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.index).encode('utf-8') +
                   str(self.content).encode('utf-8'))
        return sha.hexdigest()


    # def build_merkle_tree(self, blocks):
    #     self.merkle_tree = self._build_merkle_tree_recursive(blocks)

    # def _build_merkle_tree_recursive(self, blocks):
    #     if len(blocks) == 1:
    #         return blocks[0]

    #     next_level = []
    #     for i in range(0, len(blocks), 2):
    #         block1 = blocks[i]
    #         if i + 1 < len(blocks):
    #             block2 = blocks[i + 1]
    #             combined_hash = self.calculate_hash(block1.hash + block2.hash)
    #             parent = Block('', 0, -1, combined_hash)
    #             parent.left = block1
    #             parent.right = block2
    #             next_level.append(parent)
    #         else:
    #             next_level.append(block1)

    #     return self._build_merkle_tree_recursive(next_level)

    # def view_merkle_tree(self):
    #     self._view_merkle_tree_recursive(self.merkle_tree, 0)

    # def _view_merkle_tree_recursive(self, node, level):
    #     if node is None:
    #         return

    #     indent = '    ' * level
    #     print(indent + f"Level {level}: Hash = {node.hash}")
    #     self._view_merkle_tree_recursive(node.left, level + 1)
    #     self._view_merkle_tree_recursive(node.right, level + 1)



    def __str__(self):
        return f"previous hash: #{self.previous_hash} [hash: {self.hash}, time: {self.timestamp}, index: {self.index}, content: {self.content} ]"

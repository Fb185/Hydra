
class Ledger:
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    def get_block(self, index):
        if index < len(self.blocks):
            return self.blocks[index]
        else:
            return None

    def get_all_blocks(self):
        return self.blocks

    def get_block_count(self):
        return len(self.blocks)

    def print_ledger(self):
        for block in self.blocks:
            print(block)
            print("--------------------")
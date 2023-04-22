class Task():
    def __init__(self, description, author, id):
        self.description = description
        self.accepted_nodes = [None, None]
        self.author = author
        self.id = int(id)
        self.complete = False
        self.full = False

    def __str__(self):
        return f"Task ID: {self.id}\nDescription: {self.description}\nAuthor: {self.author}\nAccepted Nodes: {self.accepted_nodes}\nComplete: {self.complete}\nFull: {self.full}\n"

    def get_id(self):
        return int(self.id)

    def accept_node(self, node_port):
        if len(self.accepted_nodes) >= 2:
            self.full = True
        else:
            self.accepted_nodes.append(node_port)




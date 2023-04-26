class Task():
    def __init__(self, description, author, id):
        self.description = description
        self.accepted_nodes = [None, None]
        self.author = author
        self.id = int(id)
        self.complete = False

    @classmethod
    def from_string(cls, task_str):
        task_data = task_str.split(":")
        task_id = int(task_data[0])
        description = task_data[1]
        author = int(task_data[2])
        accepted_nodes = [int(node) if node != "None" else None for node in task_data[3].split(",")]
        complete = task_data[4] == "True"

        task = cls(description, author, task_id)
        task.accepted_nodes = accepted_nodes
        task.complete = complete

        return task
    def __str__(self):
        return f"Task ID: {self.id}\nDescription: {self.description}\nAuthor: {self.author}\nAccepted Nodes: {self.accepted_nodes}\nComplete: {self.complete}\n"

    def get_id(self):
        return int(self.id)

    def accept_node(self, node_port):
        if len(self.accepted_nodes) >= 2:
            self.full = True
        else:
            self.accepted_nodes.append(node_port)




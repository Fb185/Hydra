class Task():


    def __init__(self, id,description, author, assigned_nodes, validator, difficulty):
        self.id = int(id)
        self.description = description
        self.author = author
        self.complete = False
        self.assigned_nodes = assigned_nodes
        self.validator = validator
        self.difficulty = difficulty

    def from_string(task_str):
        task_data = task_str.split(":")
        task_id = int(task_data[0])
        description = task_data[1]
        author = int(task_data[2])
        assigned_nodes = [int(node) if node != "None" else None for node in task_data[3].split(",")]
        complete = task_data[4] == "True"
        validator = task_data[5]
        difficulty = task_data[7]
        task = Task(task_id, description, author, assigned_nodes, validator, difficulty)
        task.complete = complete
        return task

    def get_author(self):
        return self.author


    def check_completed(self):
        if len(self.completed_nodes) == len(self.assigned_nodes):
            self.complete = True

    def __str__(self):
      return f"Task ID: {self.id}\nDescription: {self.description}\nAuthor Node: {self.author}\nAssigned Nodes: {self.assigned_nodes}\nComplete: {self.complete}\nValidator :{self.validator}\nDifficulty :{self.difficulty}"

"""
    def get_id(self):
        return int(self.id)

    def accept_node(self, node_port):
        if len(self.assigned_nodes) >= 4:
            self.full = True
        else:
            self.assigned_nodes.append(node_port)
"""



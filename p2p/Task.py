class Task():
    def __init__(self, description, author, assigned_nodes, id):
        self.description = description
        self.author = author
        self.id = int(id)
        self.complete = False
        self.assigned_nodes = assigned_nodes
        self.completed_nodes = set()
        self.task_history = []

    def from_string(task_str):
        task_data = task_str.split(":")
        task_id = int(task_data[0])
        description = task_data[1]
        author = int(task_data[2])
        assigned_nodes = [int(node) if node != "None" else None for node in task_data[3].split(",")]
        complete = task_data[4] == "True"
        task = Task(description, author, assigned_nodes, task_id)
        task.complete = complete
        return task

    def check_completed(self):
        if len(self.completed_nodes) == len(self.assigned_nodes):
            self.complete = True
    
    def __str__(self):
        return f"Task ID: {self.id}\nDescription: {self.description}\nAuthor: {self.author}\nAssigned Nodes: {self.assigned_nodes}\nComplete: {self.complete}\n"

    def list_task_history(self):
        for task in self.task_history:
            print(str(task))

            
"""
    def get_id(self):
        return int(self.id)

    def accept_node(self, node_port):
        if len(self.assigned_nodes) >= 4:
            self.full = True
        else:
            self.assigned_nodes.append(node_port)
"""



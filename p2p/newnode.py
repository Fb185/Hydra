import socket
import threading

class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connections = []
        self.task_queue = []
        self.task_acceptors = {}
        self.lock = threading.Lock()
        self.shutdown = False 

    def __del__(self):
        self.close()

    def accept_task(self, task_id, addr):
    #     with self.lock:
    #         if task_id not in self.task_acceptors:
    #             self.task_acceptors[task_id] = []
    #         self.task_acceptors[task_id].append(addr)
        for task in self.task_queue:
            if (task == []):
                print("No tasks to accept")
                self.task_acceptors[task_id] = []
            else:
                self.task_acceptors[task_id].append(addr)
                
    def show_tasks(self):
        return self.task_queue and self.task_acceptors and self.task_acceptors
            

    def connect_to_node(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        self.connections.append(client)

        thread = threading.Thread(target=self.handle_client, args=(client, (host, port)))
        thread.start()
        print(f"Connection successfully {host}:{port}")

    def listen_for_connections(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()

        while not self.shutdown:  # Modify this line
            client, addr = server.accept()
            self.connections.append(client)
            thread = threading.Thread(target=self.handle_client, args=(client, addr))
            thread.start()

    def close(self):
        self.running = False
        for t in self.threads:
            t.join()
        self.server.close()


    # Modify the handle_client method in the Node class in newnode.py
    def handle_client(self, client, addr):
        try:
            while True:
                msg = client.recv(1024).decode('utf-8')
                if not msg:
                    break  # client closed the connection
                if msg.startswith('TASK:'):
                    print(msg)
                elif msg.startswith('YES:'):
                    task_id = int(msg.split(':')[1])
                    self.accept_task(task_id, addr)
                elif msg == 'quit':
                    break
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            if client in self.connections:
                self.connections.remove(client)
            client.close()


    def broadcast(self, msg):
        for connection in self.connections:
            # try:
            connection.send(msg.encode('utf-8'))
            # except:
            #     connection.close()
            #     self.connections.remove(connection)

    def send_message(self, host, port, msg):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        client.send(msg.encode('utf-8'))
        client.close()

    def request_task(self, task_id):
        msg = f"TASK:{task_id}:Do you want to accept task {task_id}?"
        for connection in self.connections:
            host, port = connection.getpeername()
            self.send_message(host, port, msg)
        self.task_acceptors[task_id] = []

    def start(self):
        listen_thread = threading.Thread(target=self.listen_for_connections)
        listen_thread.start()

        while True:
            command = input()
            if command.startswith("connect"):
                _, host, port = command.split()
                self.connect_to_node(host, int(port))
            elif command.startswith("task"):
                _, task_id = command.split()
                self.request_task(task_id)
            elif command.startswith("yes"):
                _, task_id = command.split()
                self.broadcast(f"YES:{task_id}")
                # self.accept_task(task_id, self.host, self.port))
            elif command.startswith("show"):
                self.show_tasks()
            else:
                self.broadcast(command)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = int(input("Enter your port number: "))

    node = Node(host, port)
    node.start()

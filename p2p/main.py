from Node import *
from tkinter import ttk
import tkinter as tk
from Node import Node


def run_gui(node):
    def on_task_select(event):
        selected_task = task_listbox.get(task_listbox.curselection())
        task_id = int(selected_task.split(':')[1])
        for task in node.available_tasks:
            if task.id == task_id:
                task_info.delete(1.0, tk.END)
                task_info.insert(tk.END, str(task))
                break

    root = tk.Tk()
    root.title("Node Task Manager")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    task_listbox = tk.Listbox(frame)
    for task in node.available_tasks:
        task_listbox.insert(tk.END, f"Task ID: {task.id}: {task.description}")
    task_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    task_listbox.bind('<<ListboxSelect>>', on_task_select)

    task_info = tk.Text(frame, wrap="word", width=40, height=10)
    task_info.grid(row=0, column=1, padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))

    root.mainloop()
def main():
    port = 8000
    while True:
        try:
            node = Node(port)
            break
        except Exception as e:
            port += 1

    print(f"Node started on port {port}")
    node.connect_to_peers()
    node.send_message(f"\nNode {port} has connected to the network")

    threading.Thread(target=node.listen).start()
    while True:
        command = input("Enter command (send/exit/make/list(available)(my)/accept)/gui: ")
        if command == "send":
            msg = input("Enter message: ")
            node.send_message(f"\nNode {port}: {msg}")

        elif command == "make":
            descriprion = input("Enter a description ")
            node.make_task(descriprion)

        elif command == "list":
            node.list_available_tasks()

        elif command == "lista":
            node.list_accepted_tasks()

        elif command == "listm":
            node.list_my_tasks()

        elif command == "accept":
            task_id = input("Enter a task ID ")
            node.accept_task(task_id)

        elif command == "gui":
            run_gui(node)

        elif command == "exit":
            node.send_message(f"Node {port} has disconnected from the network")
            node.closed = True
            node.server_socket.close()
            sys.exit()


if __name__ == "__main__":
    main()

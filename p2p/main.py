from Node import *
from tkinter import ttk
import tkinter as tk
from Task import Task


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

    if len(sys.argv) < 2:
        print("Usage: python main.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    if port < 8000 or port > 9000:
        print("incorrect port attributed.\n")
        sys.exit(1)
    
    node = Node(port)

    if not node.is_port_available():
        print("\nUnavaible port")
        sys.exit(1)
    else:
        print(f"\nNode started on port {port}")
        node.start()
        node.send_message(f"\nNode {port} has connected to the network.")
        threading.Thread(target=node.listen).start()
        

    while True:
        command = input("\nTEMPORARY MENU\n\nCommand list: send, make, list, listh, listm, balance, stake, addstake\n\n- ")

        if command == "send":
            msg = input("Enter message: ")
            node.send_message(f"\nNode {port}: {msg}")

        elif command == "make":
            #Enquanto testo as task isto fica em comentário

            if len(node.peers) < 4:
                print("\nNot enough connected nodes to create a task.")
                continue  # Skip task creation if there are not enough connected nodes
            else:
                description = input("Enter a description ")
                node.make_task(description)

        elif command == "list":
            node.list_given_tasks()

        elif command == "listh":
            Task().list_task_history()

        elif command == "listm":
            node.list_my_tasks()
                
        elif command == "gui":
            run_gui(node)

        elif command == "balance":
            node.get_balance()

        elif command == "stake":
            node.get_stake()
        
        elif command == "addstake":
            tokens = command.split(" ")[1] 
            if tokens.isdigit():
                tokens = int(tokens)
                if tokens <= node.get_balance():
                    node.add_stake(tokens)
                    print("Tokens added to stake successfully.")
                else:
                    print("Insufficient tokens in balance.")
            else:
                print("Invalid amount. Please enter a valid integer.")
        
        elif command == "exit":
            node.send_message(f"\nNode {port} has disconnected from the network.")
            node.closed = True  # Call the close method to perform cleanup tasks
            print(f"\nNode {port} disconnected.")
            sys.exit()


if __name__ == "__main__":
    main()

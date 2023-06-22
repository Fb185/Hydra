import flask
from Node import *
from tkinter import ttk
import tkinter as tk
from Blockchain import *

# app = Flask(__name__)
# @app.route("/")
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


    # peers = node.get_peers()
    # given_tasks = node.get_given_tasks()
    # render_template("index.html", peers=peers, given_tasks=given_tasks)

    # app.run()


    while True:
        command = input("\nTEMPORARY MENU\n\nCommand list:\n\nsend\nmake\nlistg\nlistm\nbalance\nstake\naddstake\n\n- ")

        if command == "send":
            msg = input("Enter message: ")
            node.send_message(f"\nNode {port}: {msg}")

        elif command == "make":

            if len(node.peers) < 4:
                print("\nNot enough connected nodes to create a task.")
                continue  # Skip task creation if there are not enough connected nodes
            else:
                description = input("Enter a description ")
                node.make_task(description)

        elif command == "listg":
            node.list_given_tasks()

        elif command == "listm":
            node.list_my_tasks()

        elif command == "balance":
            node.get_balance()

        elif command == "stake":
            node.print_stake()

        elif command == "addstake":
            node.add_stake()

        elif command == "validate":
            block = input("Enter what block you want to see: ")
            blockchain.get_block(block)

        elif command =="show":
            node.view_blockchain()




        elif command == "e":
            node.send_message(f"\nNode {port} has disconnected from the network.")
            node.closed = True  # Call the close method to perform cleanup tasks
            print(f"\nNode {port} disconnected.")
            sys.exit()


if __name__ == "__main__":
    main()


from Node import Node
from main import *
import tkinter as tk
from tkinter import *
from tkinter import ttk

class karl( Frame ):
    def __init__( self ):
        tk.Frame.__init__(self)
        self.pack()
        self.node = Node(13991)

        self.node.connect_to_peers()
        self.node.send_message(f"\nNode 13991 has connected to the network")
        # self.node = None
        # teste(self.node)

        self.master.title("Karlos")
        self.button1 = Button( self, text = "CLICK HERE", width = 25,
                               command = self.send_message )
        self.button1.grid( row = 0, column = 1, columnspan = 2, sticky = W+E+N+S )

    def send_message(self):
        self.node.send_message(f"\nNode says hi")
        print("Message sent")





def main():
    karl().mainloop()
if __name__ == '__main__':
    main()



        # if command == "send":
        #     msg = input("Enter message: ")
        #     node.send_message(f"\nNode {port}: {msg}")

        # elif command == "make":

        #     if len(node.peers) < 4:
        #         print("\nNot enough connected nodes to create a task.")
        #         continue  # Skip task creation if there are not enough connected nodes
        #     else:
        #         description = input("Enter a description ")
        #         node.make_task(description)

        # elif command == "listg":
        #     node.list_given_tasks()

        # elif command == "listm":
        #     node.list_my_tasks()

        # elif command == "balance":
        #     node.get_balance()

        # elif command == "stake":
        #     node.print_stake()

        # elif command == "addstake":
        #     node.add_stake()

        # elif command == "validate":
        #     block = input("Enter what block you want to see: ")
        #     blockchain.get_block(block)

        # elif command =="show":
        #     node.view_blockchain()




        # elif command == "e":
        #     node.send_message(f"\nNode {port} has disconnected from the network.")
        #     node.closed = True  # Call the close method to perform cleanup tasks
        #     print(f"\nNode {port} disconnected.")
        #     sys.exit()


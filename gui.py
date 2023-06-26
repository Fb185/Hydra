
import random, time
from Node import Node
import tkinter as tk
from tkinter import *
from tkinter import ttk

class karl( Frame ):
    def __init__( self ):
        tk.Frame.__init__(self)
        self.pack()
        # self.master.title("Karlos")
        port = 8000
        while True:
            try:
                print(port)
                node = Node(port, self)
                break
            except:
                port += 1

        self.node = node
        self.node.connect_to_peers()
        self.node.send_message(f"\nNode {port} has connected to the network")

        #things for send message

        self.send_button = Button(self, text = "Send", width = 25, command = self.send_message)
        self.send_button.grid(row = 0, column = 0, sticky = W+E+N+S)

        self.listg_button = Button(self, text = "listG", width = 25, command = self.listg)
        self.listg_button.grid(row = 1, column = 0, sticky = W+E+N+S)

        self.listm_button = Button(self, text = "listM", width = 25, command = self.listm)
        self.listm_button.grid(row = 2, column = 0, sticky = W+E+N+S)

        self.balance_button = Button(self, text = "Get balance", width = 25, command = self.get_balance)
        self.balance_button.grid(row = 3, column = 0, sticky = W+E+N+S)

        self.stake_button = Button(self, text = "get stake", width = 25, command = self.stake)
        self.stake_button.grid(row = 4, column = 0, sticky = W+E+N+S)

        self.add_stake_button = Button(self, text = "add stake", width = 25, command = self.add_stake)
        self.add_stake_button.grid(row = 5, column = 0, sticky = W+E+N+S)

        self.show_button = Button(self, text = "show", width = 25, command = self.show)
        self.show_button.grid(row = 6, column = 0, sticky = W+E+N+S)

        self.show_peers_button = Button(self, text = "Show peers", width = 25, command = self.show_peers)
        self.show_peers_button.grid(row = 7, column = 0, sticky = W+E+N+S)

        self.exit = Button(self, text = "Exit", width = 25, command = self.exit)
        self.exit.grid(row = 8, column = 0, sticky = W+E+N+S)

        #make a text box that is scrollable
        from tkinter import scrolledtext
        self.text_box = scrolledtext.ScrolledText(self, wrap=tk.WORD, width = 50, height = 20)
        self.text_box.grid(row = 0, column = 1, rowspan = 8, sticky = W+E+N+S)


        self.input_box = Entry(self)
        self.input_box.grid(row = 8, column = 1, rowspan = 1, sticky = W+E+N+S)
        self.input_box.insert(0, "Enter stake here")


        self.make_task_button = Button(self, text = "Make task", width = 25, command = self.make_task)
        self.make_task_button.grid(row = 0, column = 2, sticky = W+E+N+S)

        self.input_box2 = Entry(self)
        self.input_box2.grid(row = 1, column = 2, rowspan = 1, sticky = W+E+N+S)
        self.input_box2.insert(0, "Enter task here")

        #make a multiple choice section with 3 check boxes where the user can only choose one
        #use radio buttons
        self.var = IntVar()
        self.var.set(0)
        self.radio_button1 = Radiobutton(self, text = "Tier A = 5$", variable = self.var, value = 5)
        self.radio_button1.grid(row = 2, column = 2, sticky = W+E+N+S)
        self.radio_button2 = Radiobutton(self, text = "Tier B = 10$", variable = self.var, value = 10)
        self.radio_button2.grid(row = 3, column = 2, sticky = W+E+N+S)
        self.radio_button3 = Radiobutton(self, text = "Tier C = 15$", variable = self.var, value = 15)
        self.radio_button3.grid(row = 4, column = 2, sticky = W+E+N+S)


        self.image = PhotoImage(file = "logo.png")
        self.image_label = Label(self, image = self.image)
        self.image_label.grid(row = 6, column = 2, rowspan = 2, sticky = W+E+N+S)

    def listg(self):
        tasks = self.node.list_given_tasks()
        self.text_box.insert(END, f"\nList of given tasks: {tasks}\n")

    def listm(self):
        tasks = self.node.list_my_tasks()
        self.text_box.insert(END, f"\nList of my tasks: {tasks}\n")

    def stake(self):
        stake = self.node.get_stake()
        self.node.get_stake()
        self.text_box.insert(END, f"\nMy stake is {stake}\n")

    def get_balance(self):
        print("get balance")
        balance = self.node.get_balance()
        self.text_box.insert(END, f"\nMy balance is {balance}\n")

    def add_stake(self):
        #if the stake is abore the balance, then the user can't add stake
        stake = self.input_box.get()
        if stake == "":
            stake = 0
        if int(stake) > int(self.node.get_balance()):
            self.text_box.insert(END, "\nNot enough balance to add stake\n")
        self.node.add_stake(int(stake))
        self.input_box.delete(0, END)
        self.text_box.insert(END, "\nStake added!")
        self.send_button["state"] = DISABLED
        self.after(3000, self.enable_send_button)

    def show(self):
        blocks = self.node.view_blockchain()
        self.text_box.insert(END, f"\nShow: {blocks}")

    def send_purchase_msg(self):
        msg = "Task purchased"
        self.add_message(msg)

    def send_error_msg(self):
        msg = "not enough balance"
        self.add_message(msg)

    def add_message(self, message):
        self.text_box.insert(END, f"\n{str(message)}")

    def show_peers(self):
        peers = self.node.show_peers()
        self.text_box.insert(END, f"\nShow peers: {peers}")


    def send_message(self):
        msg = self.input_box.get()
        self.node.send_message(f"\nmsg: {msg}")
        self.input_box.delete(0, END)
        self.text_box.insert(END, "\nMessage sent!")
        self.send_button["state"] = DISABLED
        self.after(3000, self.enable_send_button)

    def enable_send_button(self):
        self.send_button["state"] = NORMAL


    def disable_buttons(self):
        self.exit.grid(row = 8, column = 0, sticky = W+E+N+S)
        self.send_button["state"] = DISABLED
        self.make_task_button["state"] = DISABLED
        self.listg_button["state"] = DISABLED
        self.listm_button["state"] = DISABLED
        self.balance_button["state"] = DISABLED
        self.stake_button["state"] = DISABLED
        self.add_stake_button["state"] = DISABLED
        self.show_button["state"] = DISABLED
        self.show_peers_button["state"] = DISABLED
        # self.exit["state"] = DISABLED
        self.after(10000, self.enable_buttons)


    def enable_buttons(self):
        self.send_button["state"] = NORMAL
        self.listg_button["state"] = NORMAL
        self.listm_button["state"] = NORMAL
        self.balance_button["state"] = NORMAL
        self.make_task_button["state"] = NORMAL
        self.stake_button["state"] = NORMAL
        self.add_stake_button["state"] = NORMAL
        self.show_button["state"] = NORMAL
        self.show_peers_button["state"] = NORMAL
        # self.exit["state"] = NORMAL





    def exit(self):
        self.node.server_socket.close()
        self.node.send_remove_peer()
        self.master.destroy()

    def make_task(self):
            if len(self.node.peers) < 4:
                # print("\nNot enough connected nodes to create a task.")
                message = f"\nNot enough connected nodes to create a task."
                self.add_message(message)
                # pass  # Skip task creation if there are not enough connected nodes
            else:
                description = self.input_box2.get()
                selection = self.var.get()
                if self.var.get() == 0:
                    message = f"\nPlease select a tier"
                    self.add_message(message)
                elif self.node.balance < selection:
                    message = f"\nNot enough balance to create task"
                    self.add_message(message)

                else:
                    print(selection)
                    message = f"\nTask created with description: {description} and selection: {selection}"
                    self.add_message(message)
                    self.disable_buttons()
                    self.node.make_task(description, selection)



    def working_on_task(self):
        # write on text box for 3 seconds that it is working on a task and disable the send button
        #clear the text box
        # self.text_box.delete(1.0, END)
        self.text_box.insert(END, "\nWorking on task...")
        # timer_duration = random.randint(1, 10)
        # write a for loop that adds dots to the text box every second for 3 seconds
        # for i in range(timer_duration):
        #     self.text_box.insert(END, ".")
        #     self.after(1000)
        self.make_task_button["state"] = DISABLED
        self.after(11000, self.task_done)
        self.node.send_task_done_from_gui()

    def task_done(self):
        self.text_box.insert(END, "\nTask done!")
        # self.after(1000, self.text_box.delete(1.0, END))
        self.make_task_button["state"] = NORMAL



    def disable_all_inputs(self):
        self.send_button["state"] = DISABLED
        self.input_box["state"] = DISABLED




def start_gui():
    karl().mainloop()
if __name__ == '__main__':
    start_gui()



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


from Node import *
from Blockchain import *
from gui import *

def main(interfaceString):
    interfaceString = input("Enter the interface you want to use: ")
    if interfaceString == "gui":
        start_gui()
    elif interfaceString == "terminal":
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


        # create_window(node, port)



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
                    print("""
                    Welcome to the Menu:
                    Please select an option:
                    1. Tier A - $5
                    2. Tier B - $10
                    3. Tier C - $15
                    """)

                    selected_option = input("Option: ")
                    if selected_option == '1':
                        selected_option = 5
                    elif selected_option == '2':
                        selected_option = 10
                    elif selected_option == '3':
                        selected_option = 15
                    else:
                        print("Invalid Option")
                        break
                    node.make_task(description, selected_option)

            elif command == "listg":
                node.list_given_tasks()

            elif command == "listm":
                node.list_my_tasks()

            elif command == "balance":
                node.get_balance()

            elif command == "stake":
                node.print_stake()

            elif command == "addstake":
                stake = input("how much do you want to stake: ")
                node.add_stake(stake)

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
    main(None)

# P2P Super Computer Prototype Manual

This is a prototype of a P2P supercomputer backed by a proof-of-stake blockchain.

## Usage Steps

### Requirements

- Clone the repository from the specified URL.

- Install the required dependency `tmux`.

### Graphical User Interface (GUI) Setup

1. On the virtual machine desktop, locate the file `project.sh`.
2. Click the `project.sh` icon the same number of times as the desired number of different nodes 
3. The GUI windows will open, and the P2P supercomputer prototype will be initialized.
> at least 5 GUI windows are recommended.

### Manual Setup

1. Open a terminal and navigate to the `hydra/` directory.
2. Run the command `python3 main.py`.
3. The program will prompt you to choose either GUI or terminal options.
4. If you select the GUI option, the GUI application will start. Alternatively, you can run the `project_gui.py` file to start the GUI application directly.

### Tmux Panes

1. After the simulation is set up, you will have multiple Tmux panes representing different nodes.
2. Use `Control + a` and the arrow keys or the mouse to navigate between the Tmux panes.

### Task Management

> Note: At least one node must have staked tokens on the network for a task to be created.

#### Graphical User Interface (GUI)

The GUI provides buttons for each of the task management functions:

- **Send a Message**: Enter the text in the input area at the bottom and click the **Send** button.

- **Add Stake**: Enter the amount of stake in the bottom input area and click the **Add Stake** button.

- **Make a Task**: 
  - Enter the task description in the input box below the **Make Task** button.
  - Choose one of the three tiers available.
  - Only after typing the description and choosing a tier, click the **Make Task** button.

- Additional GUI buttons:

  - **Balance**: Click the **Balance** button to view the current balance.

  - **Stake**: Click the **Stake** button to view the current stake.

  - **ListG**: Click the **ListG** button to list the submitted tasks.

  - **ListM**: Click the **ListM** button to list the tasks requested by the current node.

  - **Show**: Click the **Show** button to print out the blockchain.

  - **Show Peers**: Click the **Show Peers** button to display the connected peers.

#### Terminal Instructions

For non-GUI users, the following commands can be used:

- To send a message: Enter the message text as an argument of the `send_message` command.

- To add stake: Enter the amount of stake as an argument of the `add_stake` command.

- To make a task: Enter the task description as an argument of the `make_task` command, followed by the desired tier (1, 2, or 3) as a separate argument.

#### Additional Commands (Terminal)

For both GUI and terminal users, the following commands can be used:

- `balance`: View the balance.

- `stake`: View the stake.

- `listg`: List the submitted tasks.

- `listm`: List the tasks requested by the current node.

- `show`: Print out the blockchain.

- `showpeers`: Display the connected peers.

Please refer to the instructions above to set up and utilize the P2P supercomputer prototype effectively.

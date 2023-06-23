
# P2P Super Computer Prototype Manual

This is a prototype of a P2P supercomputer backed by a proof-of-stake blockchain.

## Usage Steps

### Requirements

- Clone the repository from the specified URL:

- Install the required dependency `tmux`:

### Simulation Setup

1. Navigate to the project directory:

2. Create a Tmux session by running the command:

3. Create 5 Tmux panes to represent different nodes:
- Press `Control + a` and then `%` (run this command twice).

4. Create a horizontal split pane:
- Press `Control + a` and then `"`.

5. Navigate to the left pane:
- Press `Control + a` and then the left arrow key.

6. Create another horizontal split pane:
- Press `Control + a` and then `"`.

7. Run `python3 main.py` in each pane to start the simulation.

8. Use `Control + a` and arrow keys or the mouse to navigate between panes.

### Task Management

- At least one node must have staked tokens on the network for a task to be created.

- To add stake on a specified node:
  - Navigate to that node.
  - Type `addstake` followed by the return key and the amount of coins to stake.

- Once there is at least one node staking coins, issue a new task:
  - Type `make` followed by the return key.
  - Enter a description of the task followed by the return key.
  - Enter a number (1, 2, or 3) corresponding to the price of the task.
  - The task will be submitted, and other nodes will enter working mode while the requesting node becomes locked until all nodes complete the task.


- Additional commands:
- `balance`: View the balance.
- `stake`: View the stake.
- `listg`: List the submitted tasks.
- `listm`: List the tasks requested by the current node.
- `show`: Print out the blockchain.

const net = require('net');
var readline = require('readline');
var crypto = require('crypto');
// Define the Block class, which represents a block in the blockchain.
function askQuestion(question) {
    return new Promise((resolve) => {
        rl.question(question, (answer) => {
            resolve(answer);
        });
    });
}
class Block {
    constructor(index, transactions, previousBlockHash) {
        this.index = index;
        this.timestamp = Date.now();
        this.transactions = transactions;
        this.previousBlockHash = previousBlockHash;
        this.difficulty = 1;
        this.nonce = 0;
        this.hash = this.calculateHash();
    }

    calculateHash() {
        const data = '${this.index}${this.timestamp}${JSON.stringify(this.transactions)}${this.previousBlockHash}${this.difficulty}${this.nonce}';
        const hash = crypto.createHash('sha256');
        hash.update(data);
        return hash.digest('hex');
    }

    mine(difficulty) {
        const target = '0'.repeat(difficulty);
        while (this.hash.substring(0, difficulty) !== target) {
            this.nonce++;
            this.hash = this.calculateHash();
        }
    }
}

// Initialize the blockchain with the genesis block.
const genesisBlock = new Block([], '0'.repeat(64));
const blockchain = [genesisBlock];

// Define the Node class, which represents a single node in the network.
class Node {
    constructor(id) {
        this.id = id;
        this.peers = [];
        this.pendingTransactions = [];
    }

    connect(peer) {
        this.peers.push(peer);
    }

    receiveTransaction(transaction) {
        this.pendingTransactions.push(transaction);
        console.log('Node ${this.id} received a new transaction from Node ${transaction.sender.id}.');
        this.broadcastTransaction(transaction);
    }

    broadcastTransaction(transaction) {
        nodes.forEach(node => {
            const socket = net.Socket();
            socket.connect(node.port, node.ip, () => {
                socket.write(`${data}\n`);
                socket.end();
            });
        });
        this.peers.forEach(peer => {
            peer.receiveTransaction(transaction);
        });
    }

    async proposeTransaction() {
        const receiverId = parseInt(await askQuestion(`Node ${this.id}, enter the ID of the receiver node: `));
        const amount = parseFloat(await askQuestion(`Node ${this.id}, enter the amount to be transferred: `));
        const receiver = nodes.find(node => node.id === receiverId);
        if (!receiver) {
            console.log('Node ${receiverId} does not exist.');
            return;
        }
        if (this === receiver) {
            console.log('Node ${this.id} cannot send money to itself.');
            return;
        }
        if (this.pendingTransactions.find(t => t.sender === this && t.receiver === receiver && t.amount === amount)) {
            console.log('Node ${this.id} has already proposed this transaction.');
            return;
        }
        if (this.pendingTransactions.find(t => t.sender === receiver && t.receiver === this && t.amount === amount)) {
            console.log('Node ${this.id} has already received this transaction.');
            return;
        }
        if (this === nodes[0] && this.pendingTransactions.length === 0) {
            console.log('Node ${this.id} is the first node to propose a transaction.');
        }
        const transaction = new Transaction(this, receiver, amount);
        this.pendingTransactions.push(transaction);
        console.log('Node ${this.id} proposed a new transaction to Node ${receiverId}.');
        this.broadcastTransaction(transaction);
    }

    mineBlock() {
        const transactions = this.pendingTransactions.slice();
        const previousBlockHash = blockchain[this.blockchainHeight - 1].hash;
        const index = this.blockchainHeight
        const block = new Block(index, transactions, previousBlockHash);
        block.mine(this.difficulty);
        blockchain.push(block);
        this.pendingTransactions = [];
        console.log('Node ${this.id} mined a new block with hash ${block.hash}.');
        this.broadcastBlock(block);
    }

    receiveBlock(block) {
        if (block.index === this.blockchainHeight) {
            if (block.previousBlockHash === blockchain[block.index - 1].hash) {
                blockchain.push(block);
                this.pendingTransactions = this.pendingTransactions.filter(t => !block.transactions.includes(t));
                console.log('Node ${this.id} received a new block with hash ${block.hash}.');
                if (this.pendingTransactions.length === 0) {
                    console.log('Node ${this.id} has caught up to the longest blockchain.');
                }
                this.broadcastBlock(block);
            } else {
                console.log('Node ${this.id} received an invalid block with hash ${block.hash}.');
            }
        } else if (block.index > this.blockchainHeight) {
            console.log('Node ${this.id} is behind the sender node.');
        } else {
            console.log('Node ${this.id} already has this block.');
        }
    }

    broadcastBlock(block) {
        nodes.forEach(node => {
            const socket = net.Socket();
            socket.connect(node.port, node.ip, () => {
                socket.write(`${data}\n`);
                socket.end();
            });
        });
        this.peers.forEach(peer => {
            peer.receiveBlock(block);
        });
    }

    startMining() {
        this.miningInterval = setInterval(() => {
            this.mineBlock();
        }, Math.floor(Math.random() * 10000) + 5000);
    }

    stopMining() {
        clearInterval(this.miningInterval);
    }

    get blockchainHeight() {
        return blockchain.length;
    }

    get difficulty() {
        const latestBlock = blockchain[this.blockchainHeight - 1];
        if (this.blockchainHeight % 5 === 0) {
            const elapsedTime = (Date.now() - latestBlock.timestamp) / 1000;
            if (elapsedTime < 30) {
                return latestBlock.difficulty + 1;
            } else if (elapsedTime > 60) {
                return Math.max(1, latestBlock.difficulty - 1);
            }
        }
        return latestBlock.difficulty;
    }

    printBlockchain() {
        console.log('Blockchain of Node ${ this.id }: ');
        blockchain.forEach(block => {
            console.log('Block ${ block.index } with hash ${ block.hash } and nonce ${ block.nonce }, containing: ');
            block.transactions.forEach(transaction => {
                console.log('- Transaction from Node ${ transaction.sender.id } to Node ${ transaction.receiver.id } for ${ transaction.amount } coins. ');
            });
        });
    }
}

// Define the Transaction class, which represents a single transaction in the blockchain.
class Transaction {
    constructor(sender, receiver, amount) {
        this.sender = sender;
        this.receiver = receiver;
        this.amount = amount;
    }
}

// Create an array of nodes, each with a unique ID.
const nodes = [new Node(1)];


function connectToNetwork() {
    const node = new Node(nodes.length + 1);
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    console.log('Connecting Node ${ node.id } to the network...');
    rl.question('Enter the IP address of an existing node: ', ip => {
        const existingNode = nodes.find(node => node.ip === ip && node.port === nextPort);
        if (existingNode) {
            node.ip = ip;
            node.port = ++nextPort;
            existingNode.connect(node);
            node.connect(existingNode);
            nodes.push(node);
            console.log(`Node ${node.id} connected to Node ${existingNode.id} with IP address ${ip} and port ${node.port}.`);
            rl.close();
        } else {
            console.log('Invalid IP address and/or port.');
            rl.close();
        }
    });
}
// Define a function to start mining on a node.
function startMining() {
    const nodeId = parseInt(readline.question('Enter the ID of the node to start mining: '));
    const node = nodes.find(node => node.id === nodeId);
    if (!node) {
        console.log('Node ${ nodeId } does not exist.');
    } else if (node.pendingTransactions.length === 0) {
        console.log('Node ${ nodeId } has no transactions to mine.');
    } else {
        node.startMining();
        console.log('Node ${ nodeId } started mining.');
    }
}

// Define a function to stop mining on a node.
function stopMining() {
    const nodeId = parseInt(readline.question('Enter the ID of the node to stop mining: '));
    const node = nodes.find(node => node.id === nodeId);
    if (!node) {
        console.log('Node ${ nodeId } does not exist.');
    } else {
        node.stopMining();
        console.log('Node ${ nodeId } stopped mining.');
    }
}

// Define a function to print the blockchain of a node.
function printBlockchain() {
    const nodeId = parseInt(readline.question('Enter the ID of the node to print the blockchain: '));
    const node = nodes.find(node => node.id === nodeId);
    if (!node) {
        console.log('Node ${ nodeId } does not exist.');
    } else {
        node.printBlockchain();
    }
}

// Start the simulation by prompting the user to create the first node.
console.log('Welcome to the Proof-of-Stake blockchain simulation!');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
rl.question('Enter the IP address of the first node: ', ip => {
    const port = parseInt(readline.question('Enter the port of the first node: '));
    nodes[0].ip = ip;
    nodes[0].port = port;
    console.log('Node 1 created with IP address ${ ip } and port ${ port }.');
    rl.close();
});

// Set up event listeners for user input.
process.stdin.setEncoding('utf8');
process.stdin.on('readable', () => {
    const chunk = process.stdin.read();
    if (chunk !== null) {
        const input = chunk.trim();
        switch (input) {
            case 'connect':
                connectToNetwork();
                break;
            case 'mine':
                startMining();
                break;
            case 'stop':
                stopMining();
                break;
            case 'print':
                printBlockchain();
                break;
            case 'exit':
                console.log('Exiting the simulation...');
                process.exit();
                break;
            default:
                console.log('Invalid input: ${ input }.');
                break;
        }
    }
});

// Set up event listeners for incoming connections.
const server = net.createServer(socket => {
    console.log('Node ${ nodes.length + 1 } connected from IP address ${ socket.remoteAddress } and port ${ socket.remotePort }.');
    const node = new Node(nodes.length + 1);
    node.ip = socket.remoteAddress;
    node.port = socket.remotePort;
    nodes.push(node);
    const data = JSON.stringify({
        type: 'connect',
        peers: nodes.map(n => ({ id: n.id, ip: n.ip, port: n.port })).filter(n => n.id !== node.id)
    });
    socket.write('${ data }\n');
    socket.on('data', data => {
        const message = JSON.parse(data);
        switch (message.type) {
            case 'transaction':
                const transaction = new Transaction(nodes.find(n => n.id === message.sender.id), nodes.find(n => n.id === message.receiver.id), message.amount);
                node.receiveTransaction(transaction);
                break;
            case 'block':
                const transactions = message.transactions.map(t => new Transaction(nodes.find(n => n.id === t.sender.id), nodes.find(n => n.id === t.receiver.id), t.amount));
                const index = this.blockchainHeight
                const block = new Block(index, transactions, previousBlockHash);
                block.index = message.index;
                block.timestamp = message.timestamp;
                block.difficulty = message.difficulty;
                block.nonce = message.nonce;
                block.hash = message.hash;
                node.receiveBlock(block);
                break;
            default:
                console.log('Invalid message type: ${ message.type }.');
                break;
        }
    });
    socket.on('end', () => {
        console.log('Node ${ node.id } disconnected.');
        nodes.splice(nodes.findIndex(n => n.id === node.id), 1);
    });
});
server.on('error', err => {
    console.log('Server error: ${ err }.');
});
let nextPort = 8000
server.listen(nextPort, () => {
    console.log('Server listening on port 3000.');
});

// Define a function to broadcast a transaction to all connected peers.
function broadcastTransaction(transaction) {
    const data = JSON.stringify({
        type: 'transaction',
        sender: {
            id: transaction.sender.id,
            ip: transaction.sender.ip,
            port: transaction.sender.port
        },
        receiver: {
            id: transaction.receiver.id,
            ip: transaction.receiver.ip,
            port: transaction.receiver.port
        },
        amount: transaction.amount
    });
    const socket = net.Socket();
    nodes.forEach(node => {
        socket.connect(node.port, node.ip, () => {
            socket.write('${data}\n');
            socket.end();
        });
    });
}

// Define a function to broadcast a block to all connected peers.
function broadcastBlock(block) {
    const data = JSON.stringify({
        type: 'block',
        index: block.index,
        timestamp: block.timestamp,
        transactions: block.transactions.map(t => ({
            sender: {
                id: t.sender.id,
                ip: t.sender.ip,
                port: t.sender.port
            },
            receiver: {
                id: t.receiver.id,
                ip: t.receiver.ip,
                port: t.receiver.port
            },
            amount: t.amount
        })),
        previousBlockHash: block.previousBlockHash,
        difficulty: block.difficulty,
        nonce: block.nonce,
        hash: block.hash
    });
    const socket = net.Socket();
    nodes.forEach(node => {
        socket.connect(node.port, node.ip, () => {
            socket.write('${data}\n');
            socket.end();
        });
    });
}

// // Set up the main simulation loop to propose transactions randomly.
// setInterval(() => {
//     const sender = nodes[Math.floor(Math.random() * nodes.length)];
//     const receiver = nodes.filter(node => node !== sender)[Math.floor(Math.random() * (nodes.length - 1))];
//     const amount = Math.floor(Math.random() * 10);
//     const transaction = new Transaction(sender, receiver, amount);
//     sender.proposeTransaction(transaction);
//     broadcastTransaction(transaction);
// }, 5000);


setInterval(() => {
    const sender = nodes[Math.floor(Math.random() * nodes.length)];
    sender.proposeTransaction();
}, 5000);

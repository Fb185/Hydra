const SHA256 = require('crypto-js/sha256')

class Block {
    constructor(timestamp, medicalRecord, previousHash = '') {
        this.timestamp = timestamp;
        this.medicalRecord = medicalRecord;
        this.previousHash = previousHash;
        this.hash = this.calculateHash()
        this.nonce = 0;

    }
    calculateHash() {
        return SHA256(this.previousHash + this.timestamp + this.medicalRecord + this.nonce).toString()
        // return SHA256(this.previousHash + this.timestamp + JSON.stringify(this.medicalRecord) + this.nonce).toString()
    }

    mineBlock(difficulty) {
        while (this.hash.substring(0, difficulty) !== Array(difficulty + 1).join("0")) {
            this.nonce++;
            this.hash = this.calculateHash();
        }
        // console.log("Block mined: " + this.hash)
    }
}

class Transaction {
    constructor(fromAddress, toAddress, data) {
        this.fromAddress = fromAddress
        this.toAddress = toAddress
        this.data = data;
    }

}
class BlockChain {
    constructor() {
        this.chain = [this.createGenesisBlock()];
        this.difficulty = 0;
        this.pendingTransaction = [];
    }

    createGenesisBlock() {
        return new Block("01/07/2023", "Genesis Block", "0")
    }

    getLatestBlock() {
        return this.chain[this.chain.length - 1];
    }


    minePendingTransactions(fromAddress, toAddress, data) {
        let block = new Block(Date.now(), this.pendingTransaction)
        block.previousHash = this.getLatestBlock().hash
        block.mineBlock(this.difficulty)


        console.log("Block successfully mined")
        this.chain.push(block)
        console.log(block)
        this.pendingTransaction = []
    }

    createTransaction(fromAddress, toAddress, data) {
        let transaction = new Transaction(fromAddress, toAddress, data)
        this.pendingTransaction.push(transaction)
    }

}

let prescription = new BlockChain();

// prescription.addBlock(new Block(1, "somedate", { medication: "brufen" }));
// prescription.addBlock(new Block(2, "somedate +1", { medication: "brufen" }));
console.log("mining block 1....");
prescription.createTransaction("doctor 0", "pacient 0 ", "medication: brufen")
prescription.minePendingTransactions()
console.log("mining block 2....");
prescription.createTransaction("doctor 1", "pacient 1 ", "medication: viagra")
prescription.minePendingTransactions()
console.log("mining block 3....");
prescription.createTransaction("doctor 2", "pacient 2 ", "medication: xanax")
prescription.minePendingTransactions()


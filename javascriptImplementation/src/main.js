const {BlockChain, Transaction} = require('./blockchain');
const EC = require('elliptic').ec
const ec = new EC('secp256k1')

const myKey = ec.keyFromPrivate('719f65a4552ba29e1a253047fee1bee9982856fc27caf6c4d760857ed2746c10')
const myWalletAddress = myKey.getPublic('hex')

let coin = new BlockChain();


const tx1 = new Transaction(myWalletAddress, 'publickey goes here', 10)
tx1.signTransaction(myKey)
coin.addTransaction(tx1)

console.log('\n Starting the miner...')
coin.minePendingTransactions(myWalletAddress)
console.log('\nBalance of cav is ', coin.getBalanceOfAddress(myWalletAddress))


const tx2 = new Transaction(myWalletAddress, 'publickey goes here', 10)
tx2.signTransaction(myKey)
coin.addTransaction(tx2)

console.log('\n Starting the miner...')
coin.minePendingTransactions(myWalletAddress)
console.log('\nBalance of cav is ', coin.getBalanceOfAddress(myWalletAddress))




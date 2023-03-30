package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"log"
	"math/big"
	"strconv"
	"strings"
	"time"
)

type Block struct {
	Index        int
	Timestamp    int64
	Transactions []*Transaction
	PrevHash     string
	Hash         string
	Nonce        int
}

func (b *Block) CalculateHash() string {
	hashData := strconv.Itoa(b.Index) + strconv.FormatInt(b.Timestamp, 10) + TransactionsToStr(b.Transactions) + strconv.Itoa(b.Nonce) + b.PrevHash
	hash := sha256.New()
	hash.Write([]byte(hashData))
	return hex.EncodeToString(hash.Sum(nil))
}

const difficulty = 4

func (b *Block) ProofOfWork() {
	nonce := 0
	for {
		b.Nonce = nonce
		hash := b.CalculateHash()
		if IsHashValid(hash) {
			b.Hash = hash
			break
		}
		nonce++
	}
}

func IsHashValid(hash string) bool {
	prefix := strings.Repeat("0", difficulty)
	return strings.HasPrefix(hash, prefix)
}

type Blockchain struct {
	Blocks []*Block
}

func NewBlockchain() *Blockchain {
	genesisBlock := &Block{
		Index:        0,
		Timestamp:    time.Now().Unix(),
		Transactions: []*Transaction{},
		PrevHash:     "",
	}
	genesisBlock.ProofOfWork()

	return &Blockchain{
		Blocks: []*Block{genesisBlock},
	}
}

func (bc *Blockchain) AddBlock(transactions []*Transaction) *Block {
	prevBlock := bc.Blocks[len(bc.Blocks)-1]
	newBlock := &Block{
		Index:        prevBlock.Index + 1,
		Timestamp:    time.Now().Unix(),
		Transactions: transactions,
		PrevHash:     prevBlock.Hash,
	}
	newBlock.ProofOfWork()
	bc.Blocks = append(bc.Blocks, newBlock)
	return newBlock
}

type Transaction struct {
	ID      string
	Inputs  []TxInput
	Outputs []TxOutput
}

type TxInput struct {
	TxID      string
	OutputIdx int
	Signature string
}

type TxOutput struct {
	Value      int
	PubKeyHash string
}

type Wallet struct {
	PrivateKey ecdsa.PrivateKey
	PublicKey  ecdsa.PublicKey
}

func (w *Wallet) Generate() {
	// Generate Private/Public key pair
	curve := elliptic.P256()
	privateKey, err := ecdsa.GenerateKey(curve, rand.Reader)
	if err != nil {
		log.Panic(err)
	}

	publicKey := privateKey.PublicKey

	w.PrivateKey = *privateKey
	w.PublicKey = publicKey
}

func (w *Wallet) Sign(hash []byte) (string, error) {
	// Sign the transaction
	r, s, err := ecdsa.Sign(rand.Reader, &w.PrivateKey, hash)
	if err != nil {
		return "", err
	}

	signature := append(r.Bytes(), s.Bytes()...)

	return hex.EncodeToString(signature), nil
}

func (w *Wallet) Verify(hash []byte, signature string) bool {
	// Verify the transaction
	signatureBytes, err := hex.DecodeString(signature)
	if err != nil {
		log.Panic(err)
	}

	r := big.Int{}
	s := big.Int{}
	r.SetBytes(signatureBytes[:len(signatureBytes)/2])
	s.SetBytes(signatureBytes[len(signatureBytes)/2:])

	return ecdsa.Verify(&w.PublicKey, hash, &r, &s)
}

func NewTransaction(sender, recipient string, amount int, utxo map[string]TxOutput) *Transaction {
	acc, validOutputs := FindSpendableOutputs(sender, amount, utxo)

	if acc < amount {
		log.Panic("Error: Not enough funds")
		return nil
	}

	inputs := createTransactionInputs(sender, validOutputs)
	outputs := createTransactionOutputs(sender, recipient, amount, acc)

	tx := Transaction{ID: "", Inputs: inputs, Outputs: outputs}
	tx.ID = tx.CalculateHash()

	return &tx
}

func createTransactionInputs(sender string, validOutputs map[string][]int) []TxInput {
	inputs := make([]TxInput, 0)

	for txid, outs := range validOutputs {
		for _, outIdx := range outs {
			input := TxInput{TxID: txid, OutputIdx: outIdx, Signature: sender}
			inputs = append(inputs, input)
		}
	}

	return inputs
}

func createTransactionOutputs(sender, recipient string, amount, acc int) []TxOutput {
	outputs := make([]TxOutput, 0)

	outputs = append(outputs, TxOutput{Value: amount, PubKeyHash: recipient})

	if acc > amount {
		outputs = append(outputs, TxOutput{Value: acc - amount, PubKeyHash: sender})
	}
	return outputs
}

func (tx *Transaction) CalculateHash() string {
	hashData := ""
	for _, input := range tx.Inputs {
		hashData += input.TxID + strconv.Itoa(input.OutputIdx) + input.Signature
	}
	for _, output := range tx.Outputs {
		hashData += strconv.Itoa(output.Value) + output.PubKeyHash
	}
	hash := sha256.New()
	hash.Write([]byte(hashData))
	return hex.EncodeToString(hash.Sum(nil))
}

func FindSpendableOutputs(sender string, amount int, utxo map[string]TxOutput) (int, map[string][]int) {
	unspentOutputs := make(map[string][]int)
	accumulated := 0

	for txID, output := range utxo {
		if output.PubKeyHash == sender {
			unspentOutputs[txID] = append(unspentOutputs[txID], 1)
			accumulated += output.Value
		}

		if accumulated >= amount {
			break
		}
	}

	return accumulated, unspentOutputs
}

func TransactionsToStr(transactions []*Transaction) string {
	var result string
	for _, tx := range transactions {
		result += tx.ID
	}
	return result
}
func getBalance(publicKey ecdsa.PublicKey, blockchain *Blockchain) int {
	pubKeyHash := publicKeyHash(publicKey)
	balance := 0

	for _, block := range blockchain.Blocks {
		for _, tx := range block.Transactions {
			for _, output := range tx.Outputs {
				if output.PubKeyHash == pubKeyHash {
					balance += output.Value
				}
			}

			for _, input := range tx.Inputs {
				if input.Signature == pubKeyHash {
					// Find the corresponding output and decrease the balance
					for _, prevTx := range blockchain.Blocks {
						for _, prevOutput := range prevTx.Transactions {
							if prevOutput.ID == input.TxID {
								balance -= prevOutput.Outputs[input.OutputIdx].Value
							}
						}
					}
				}
			}
		}
	}

	return balance
}
func publicKeyHash(publicKey ecdsa.PublicKey) string {
	pubKeyBytes := elliptic.Marshal(elliptic.P256(), publicKey.X, publicKey.Y)
	hash := sha256.Sum256(pubKeyBytes)
	return fmt.Sprintf("%x", hash)
}

func main() {
// Create a new blockchain
	blockchain := NewBlockchain()

	// Create wallets for Alice and Bob
	alice := &Wallet{}
	alice.Generate()
	bob := &Wallet{}
	bob.Generate()

	// Create a transaction from Alice to Bob
	// For demonstration purposes, we will use a fake UTXO set
	fakeUTXO := map[string]TxOutput{
		"fakeTxID": {Value: 50, PubKeyHash: publicKeyHash(alice.PublicKey)},
	}

	tx := NewTransaction(publicKeyHash(alice.PublicKey), publicKeyHash(bob.PublicKey), 10, fakeUTXO)
	fmt.Println("Transaction ID:", tx.ID)

	// Add the transaction to a new block in the blockchain
	block := blockchain.AddBlock([]*Transaction{tx})
	fmt.Println("New block added with hash:", block.Hash)

	// Display the blockchain
	for i, block := range blockchain.Blocks {
		fmt.Printf("Block %d: %s\n", i, block.Hash)
	}

	// Check balances
	aliceBalance := getBalance(alice.PublicKey, blockchain)
	bobBalance := getBalance(bob.PublicKey, blockchain)

	fmt.Printf("Alice's balance: %d\n", aliceBalance)
	fmt.Printf("Bob's balance: %d\n", bobBalance)
}

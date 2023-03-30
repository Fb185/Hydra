package blockchain

import (
	"fmt"

	"github.com/dgraph-io/badger"
)

const (
	dbPath = "./tmp/blocks"
)

type BlockChain struct {
	LastHash []*Block
	Database *badger.DB
}

type BlockChainIterator struct {
	CurrentHash []byte
	Database    *badger.DB
}

func InitBLockChain() *BlockChain {
	var lastHash []byte

	opts := badger.DefaultOptions
	opts.Dir = dbPath
	opts.ValueDir = dbPath

	db, err := badger.Open(opts)
	Handle(err)

	err = db.Update(func(txn *badger.Txn) error {
		if _, err := txn.Get([]byte("lh")); err == badger.ErrKeyNotFound {
			fmt.Println("No existing blockchain yet")
			genesis := Genesis()
			fmt.Println("Genesis proved")
			err = txn.Set(genesis.hash, genesis.Serialize())

			Handle(err)
			err = txn.Set([]byte("lh"), genesis.Hash)
			lastHash = genesis.Hash
			return err
		} else {
			item, err := txn.Get([]byte("lh"))
			Handle(err)
			lastHash, err = item.Value()
			return err
		}
	})

	Handle(err)

	Blockchain := BlockChain{lastHash, db}
	return &Blockchain

}

func (chain *BlockChain) AddBlock(data string) {
	var lastHash []byte

	err := chain.Database.View(func(txn *badger.Txn) error {
		item, err := txn.Get([]byte("lh"))
		Handle(err)
		lastHash, err = item.Value()
		return err
	})
	Handle(err)
	newBlock := CreateBlock(data, lastHash)

	err = chain.Database.Update(func(txn *badger.Txn) error {
		err := txn.Set(newBlock.Hash, newBlock.Serialize())
		Handle(err)
		err = txn.Set([]byte("lh"), newBlock.Hash)

		chain.LastHash = newBlock.Hash
		return err
	})
	Handle(err)
}
func (chain *BlockChain) Iterator() *BlockChainIterator{
    iter := &BlockChainIterator{chain.LastHash, chain.Database}
    return iter
}

func (iter *BlockChainIterator) Next() *Block{
    var block *Block
    err := iter.Database.View(func(txn *badger.Txn) error{
        item, err := txn.Get(iter.CurrentHash)
        Handle(err)
        encodedBlock, err := item.Value()
        block = Deserialize(encodedBlock)
        return err
    })
    Handle(err)
    iter.CurrentHash = block.PrevHash
    return block
}

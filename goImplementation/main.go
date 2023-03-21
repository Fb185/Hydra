package main

import (
	"fmt"

	"github.com/fb185/MediChain/goImplementation/blockchain"
)


func main() {
	chain := blockchain.InitBLockChain()
	chain.AddBlock("First")
	chain.AddBlock("Second")
	chain.AddBlock("Third")

    for _, block := range chain.blocks{
        fmt.Printf("Prev hash: %x\n", block.PrevHash)
        fmt.Printf("Data in Block: %s\n", block.Data)
        fmt.Printf("Hash : %x\n", block.Hash)
    }

}

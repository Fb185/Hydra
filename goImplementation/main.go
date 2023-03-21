package main

import (
	"fmt"
	"strconv"
	"github.com/fb185/MediChain"
)

func main() {
	chain := blockchain.InitBLockChain()
	chain.AddBlock("First")
	chain.AddBlock("Second")
	chain.AddBlock("Third")

	for _, block := range chain.blocks {
		fmt.Printf("Prev hash: %x\n", block.PrevHash)
		fmt.Printf("Data in Block: %s\n", block.Data)
		fmt.Printf("Hash : %x\n", block.Hash)

		pow := blockchain.NewProof(block)
		fmt.Println("PoW: %s\n", strconv.FormatBool(pow.Validate()))
		fmt.Println()
	}

}
